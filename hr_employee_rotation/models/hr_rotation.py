from odoo import fields , api , models , _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError

class employee_rotation(models.Model):
    _name = 'employee.rotation'
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
    _description = 'Employee Rotation'
    _rec_name = 'employee_id'

    date = fields.Date("Request Date", default=datetime.datetime.now().date(), readonly=True)
    effective_date = fields.Date("Effective Date")
    approved_date = fields.Date("Approved on",readonly=True)
    employee_id = fields.Many2one("hr.employee", "Employee", required=True)
    requested_by = fields.Many2one("hr.employee", "Officer")
    transfer_type = fields.Selection([('location','Location'),('department','Department'),('company','Company')])
    department_id = fields.Many2one("hr.department","Department",)
    job_id = fields.Many2one("hr.job", "Job Title",)
    
    n_department_id = fields.Many2one("hr.department", "New Department")
    n_job_id = fields.Many2one("hr.job", "New Job Title")
    state = fields.Selection([
        ('draft','Draft'),
        ('line_manager','Line Manager Approval'),
        ('hr_officer','HR Officer Approval'),
        ('hr_manager','HR Section Head Approval'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ], default='draft',tracking=True)
    company_id = fields.Many2one("res.company", string="Company", related="employee_id.company_id", store=True,readonly=True)
    note = fields.Text("Justification",required=True)
    hr_comment = fields.Text("HR Comment")
    n_reg = fields.Many2one("hr.department",string="To Reg",domain="[('field_hq','=','field')]")

    is_manager = fields.Boolean(compute='check_manager')
    apply_new_gross = fields.Boolean("Apply New Gross ?")
    gross = fields.Float("Gross",compute='get_gross')
    new_gross = fields.Float("New Gross")
    active = fields.Boolean(string='Active', default=True)

    
    @api.depends('employee_id')
    def get_gross(self):
        for rec in self:
            rec.gross = rec.employee_id.contract_id.wage
    
    @api.depends('department_id')
    def check_manager(self):
        for rec in self:
            if rec.department_id:
                rec.is_manager = False
                if rec.department_id.manager_id.user_id.id == self.env.user.id:
                    rec.is_manager = True
                else:
                    rec.is_manager = False
            else:
                rec.is_manager = False
    

    @api.depends('employee_id.department_id','employee_id.job_id')
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            rec.department_id = rec.employee_id.department_id
            rec.job_id = rec.employee_id.job_id
            
    def line_approve(self):
        for rec in self:
            rec.state = 'hr_manager'

    def officer_approve(self):
        for rec in self:
            rec.state = 'hr_manager'
    
    def hr_officer_approve(self):
        for rec in self:
            rec.state = 'hr_officer'

    def submit_button(self):
        for rec in self:
            hr_manager_user = []
            hr_manager_user = rec.env.ref('hr.group_hr_manager').users
            hr_managers = rec.env.ref('hr.group_hr_manager').users.mapped('employee_ids')
            emails = [manager.work_email for manager in hr_managers]
            rec.requested_by = rec.env.user.employee_id
            for manager_user in hr_manager_user:
                mail_content = "  Hello  "  ",<br> There is a rotation request for employee " + str(rec.employee_id.name) \
                    + " with employee code of "  + str(rec.employee_id.emp_code) + " Please review the request for Approval."
                main_content = {
                    'subject': _('Rotation of %s') % (rec.employee_id.name),
                    'author_id': rec.env.user.partner_id.id,
                    'body_html': mail_content,
                    'email_to': emails,
                }
                rec.env['mail.mail'].sudo().create(main_content).send()
                rec.activity_schedule('hr_employee_rotation.mail_act_approval', user_id=manager_user.id)
            rec.state = 'line_manager'

    def reject_button(self):
        for rec in self:
            # officers = self.env.ref('hr.group_hr_user').users.mapped('employee_ids')
            # emails = [officer.work_email for officer in officers]
            email = rec.requested_by.work_email
            mail_content = "  Hello  "  ",<br> The rotation request for employee " + str(rec.employee_id.name) \
                + " with employee code of "  + str(rec.employee_id.emp_code) + " was rejected, please contact your HR Section Head for clarification."
            main_content = {
                'subject': _('Rotation of %s') % (rec.employee_id.name),
                'author_id': rec.env.user.partner_id.id,
                'body_html': mail_content,
                'email_to': email,
            }
            rec.env['mail.mail'].sudo().create(main_content).send()
            # rec.activity_schedule('hr_employee_rotation.mail_act_reject', user_id=rec.create_uid.id)
            rec.activity_unlink(['hr_employee_rotation.mail_act_approval'])
            rec.activity_unlink(['hr_employee_rotation.mail_act_reject'])
            rec.state = 'rejected'


    def draft_button(self):
        for rec in self:
            rec.state = 'draft'

    def hr_manager_approve(self):
        for rec in self:
            rec.state = 'approved'
            rec.approved_date = fields.Date.today()
            
    def schedule_rotation(self):
        for rec in self:
            if rec.effective_date == fields.Date.today():
                rec.sudo().employee_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
                rec.sudo().employee_id.parent_id = rec.n_department_id.manager_id if rec.n_department_id else rec.department_id.manager_id
                rec.sudo().employee_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
                if rec.sudo().employee_id.contract_id:
                    rec.sudo().employee_id.contract_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
                    rec.sudo().employee_id.contract_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
                    rec.sudo().employee_id.contract_id.wage = rec.new_gross if rec.apply_new_gross else rec.gross
                d = rec.date
                dt = datetime.datetime.strptime(str(d), "%Y-%m-%d")
                planned = self.env['work.force.planning.line'].search([('state','=','approved'),('job_position','=',rec.job_id.id)]).filtered(lambda r:datetime.datetime.strptime(str(r.date), "%Y-%m-%d").year == dt.year)
                for wfp in planned:
                    wfp.rotation += 1
                rec.activity_unlink(['hr_employee_rotation.mail_act_approval'])
                rec.activity_unlink(['hr_employee_rotation.mail_act_reject'])

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        for rec in self:
            if not rec.state == 'draft':
                raise UserError("Only draft records can be deleted!")
        
class hrEmployee(models.Model):
    _inherit = 'hr.employee'

    rotation_count = fields.Integer(compute='compute_rotation_count')
    active = fields.Boolean(string='Active', default=True)


    def compute_rotation_count(self):
        for record in self:
            record.rotation_count = self.env['employee.rotation'].search_count(
                [('employee_id', '=', self.id)])

    def get_rotation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rotation',
            'view_mode': 'tree,form',
            'res_model': 'employee.rotation',
            'domain': [('employee_id', '=', self.id)],
            'context': "{'create': False}"
        }
