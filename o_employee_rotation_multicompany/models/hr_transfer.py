from odoo import fields , api , models , _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError
from datetime import datetime, timedelta


class employee_transfer(models.Model):
    _name = 'employee.transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = 'Employee Transfer'
    _rec_name = 'employee_id'

    transfer_type = fields.Selection([('location','Location Based'),('department','Department'),('company','Company')],required=True)
    date = fields.Date("Request Date", default=datetime.now().date(), readonly=True)
    effective_date = fields.Date("Effective Date")
    approved_date = fields.Date("Approved on",readonly=True)
    employee_id = fields.Many2one("hr.employee", "Employee")
    company_id = fields.Many2one(related="employee_id.company_id", string="Company", readonly=True)
    department_id = fields.Many2one(related="employee_id.department_id",string="Department", )
    job_id = fields.Many2one(related="employee_id.job_id", string="Job Title", readonly=True)
    n_department_id = fields.Many2one("hr.department", "New Department",)
    n_job_id = fields.Many2one("hr.job", "New Job Title",)
    n_company_id = fields.Many2one("res.company", string="New Company", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('trans_manager', 'Transfer Manager Approval'),
        ('receive_manager', 'Receiving Manager Approval'),
        # ('hr_officer','HR Officer Approval'),
        ('hr_manager', 'HR Section Head Approval'),
        ('md', 'MD Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', track_visibility='onchange')
    note = fields.Text("Justification",required=True)
    hr_comment = fields.Text("Hr Comment")
    scheduled = fields.Boolean("Scheduled")
    is_manager = fields.Boolean(compute='check_manager')
    is_manager_n = fields.Boolean(compute='check_manager_n')
    apply_new_gross = fields.Boolean("Apply New Gross ?")
    gross = fields.Float("Gross",compute='get_gross')
    new_gross = fields.Float("New Gross")
    grade_id = fields.Many2one(
        'hr.grade.configuration', 'Grade', compute="_onchange_employee_id", store=True)
    n_grade_id = fields.Many2one('hr.grade.configuration', 'New Grade')

    grade = fields.Many2one(comodel_name='hr.grade.configuration', string='Grade')
    new_grade = fields.Many2one(comodel_name='hr.grade.configuration', string='New grade')
    active = fields.Boolean(string='Active', default=True)
   
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.grade_id = self.employee_id.contract_id.grade_id or False
    
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
    
    @api.depends('n_department_id')
    def check_manager_n(self):
        for rec in self:
            if rec.n_department_id:
                rec.is_manager_n = False
                if rec.n_department_id.manager_id.user_id.id == self.env.user.id:
                    rec.is_manager_n = True
                else:
                    rec.is_manager_n = False
            else:
                rec.is_manager_n = False

    #######################################
    name = fields.Char("Employee Name")
    
    @api.onchange('n_company_id')
    def dep_domain(self):
        for rec in self:
            if rec.transfer_type == 'company' and rec.n_company_id:
                return {
                    'domain': {'n_department_id': [('company_id', '=', rec.n_company_id.id)]}
                }
                
    def trans_approve(self):
        for rec in self:
            rec.state = 'receive_manager'
    
    def receive_approve(self):
        for rec in self:
            rec.state = 'hr_officer'

    def officer_approve(self):
        for rec in self:
            rec.state = 'hr_manager'
            
    def hr_approve(self):
        for rec in self:
            rec.state = 'md'

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.department_id = self.employee_id.department_id
        self.job_id = self.employee_id.job_id
        self.company_id = self.employee_id.company_id

        ####################
        #if self.employee_id:
         #   self.name = self.employee_id.name
    def submit_button(self):
        for rec in self:
            hr_manager_user = []
            hr_manager_user = rec.env.ref('hr.group_hr_manager').users
            hr_managers = rec.env.ref('hr.group_hr_manager').users.mapped('employee_ids')
            emails = [manager.work_email for manager in hr_managers]
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
            rec.state = 'trans_manager'

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
    
    


    def md_approve(self):
        for rec in self:
            rec.state = 'approved'
            rec.approved_date = fields.Date.today()
            
    def schedule_transfer(self):
        for rec in self:
            if rec.affective_date == fields.Date.today():
                rec.sudo().employee_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
                rec.sudo().employee_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
                rec.sudo().employee_id.parent_id = rec.n_department_id.manager_id if rec.n_department_id else rec.department_id.manager_id
                if rec.n_grade_id and rec.grade_id != rec.n_grade_id:
                # rec.employee_id.grade_id = rec.n_grade_id
                    rec.sudo().employee_id.contract_id.grade_id = rec.n_grade_id
                if rec.transfer_type == 'company':
                    rec.sudo().employee_id.company_id = rec.n_company_id if rec.n_company_id else rec.company_id
                if rec.transfer_type == 'location':
                    rec.sudo().employee_id.field_hq = rec.n_field_hq if rec.n_field_hq else rec.field_hq
                if rec.sudo().employee_id.contract_id:
                    rec.sudo().employee_id.contract_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
                    rec.sudo().employee_id.contract_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
                if rec.sudo().employee_id.contract_id:
                    rec.sudo().employee_id.contract_id.wage = rec.new_gross if rec.apply_new_gross else rec.gross
                d = rec.date
                dt = datetime.strptime(str(d), "%Y-%m-%d")
                planned = self.env['work.force.planning.line'].search([('state','=','approved'),('job_position','=',rec.job_id.id)]).filtered(lambda r:datetime.strptime(str(r.date), "%Y-%m-%d").year == dt.year)
                for wfp in planned:
                    wfp.transfer += 1
                rec.activity_unlink(['hr_employee_rotation.mail_act_approval'])
                rec.activity_unlink(['hr_employee_rotation.mail_act_reject'])

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    def unlink(self):
        for rec in self:
            if not rec.state == 'draft':
                raise UserError("Only draft records can be deleted!")
            
    def schedule_evaluation(self):
        transfers = self.search([('scheduled','=',False),('employee_id','!=',False),('state','=','approved')])
        email_transfers = self.search([('employee_id','!=',False),('state','=','approved')])
        users = []
        emails = []
        hr_users = self.env['res.users'].search([])
        for h in hr_users:
            if h.has_group('hr.group_hr_manager'):
                users.append(h.partner_id.id)
                emails.append(h.partner_id.email)
        for transfers in transfers:
            reminder_date = fields.Date.from_string(transfers.date) + timedelta(days=59)
            message = self.env['calendar.event'].create({
                'name': "Evaluation Reminder Of Employee("+str(transfers.employee_id.name)+")",
                'partner_ids': [(6, 0, users)],
                'alarm_ids': [(4, 5), (4, 3), (4, 2)],
                'allday': True,
                'start': reminder_date,
                'stop': reminder_date,
            }).id
            transfers.scheduled = True
        for e_transfer in email_transfers:
            reminder_e_date = fields.Date.from_string(e_transfer.date) + timedelta(days=59)
            if reminder_e_date == fields.Date.today():
                email_to = ",".join(emails)
                mail_content = "  Hello  "  ",<br> This is a reminder that the employee " + str(e_transfer.employee_id.name) \
                    + " with employee code of "  + str(e_transfer.employee_id.emp_code) + " have completed 2 months, please consider evaluation."
                main_content = {
                    'subject': _('Evaluation of %s') % (e_transfer.employee_id.name),
                    'author_id': self.env.user.partner_id.id,
                    'body_html': mail_content,
                    'email_to': email_to,
                }
                self.env['mail.mail'].sudo().create(main_content).send()