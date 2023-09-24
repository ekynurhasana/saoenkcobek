from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    basic_salary = fields.Float(string='Basic Salary')