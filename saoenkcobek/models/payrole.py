from odoo import models, fields

class payrole(models.Model):
    _name = 'payrole'
    _description = 'gaji Karyawan'

    employer_name = fields.Char(string='Employer Name', required=True)
    basic_salary = fields.Float(string='Basic Salary')
    allowance = fields.Float(string='Allowance')
    benefit = fields.Float(string='Benefit')
    deducation = fields.Float(string='deducation')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary', store=True)


    


