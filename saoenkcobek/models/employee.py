from odoo import models, fields

class employee(models.Model):
    _name = 'employee'
    _description = 'karyawan'


    employee_name = fields.Char(string='Employee Name')
    branch = fields.Char(string='Branch')
    job_position = fields.Char(string='Job Position')
    employee_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')],
        string='Employee Status', default='active')
    email = fields.Char(string='email')