
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_top_management = fields.Boolean('Top Management')

class hrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    is_top_management = fields.Boolean('Top Management')