from odoo import fields , api , models , _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError

class employee_rotation(models.Model):
    _inherit = 'employee.rotation' 

    n_company_id = fields.Many2one("res.company", string="New Company")
    
    
    # def hr_manager_approve(self):
    #     for rec in self:
    #         rec.sudo().employee_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
    #         rec.sudo().employee_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
    #         rec.sudo().employee_id.company_id = rec.n_company_id if rec.n_company_id else rec.company_id
    #         if rec.sudo().employee_id.contract_id:
    #             rec.sudo().employee_id.contract_id.department_id = rec.n_department_id if rec.n_department_id else rec.department_id
    #             rec.sudo().employee_id.contract_id.job_id = rec.n_job_id if rec.n_job_id else rec.job_id
    #         rec.state = 'hr_manager'
    
