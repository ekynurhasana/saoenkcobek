from odoo import models, fields

class overtime(models.Model):
    _name = 'overtime'
    _description = 'Lembur Karyawan'

    employee_name = fields.Many2one(string='employee name', required=True)
    request_overtime_date = fields.Date(string=" Request date")
    overtime_date = fields.Date(string="Overtime request")
    overtime_duration = fields.Float(string="Durasi Overtime")
    overtime_status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('rejected', 'Rejected')],
    string="Status Overtime",
    default='draft')


    #  @api.depends('basic_salary', 'allowance', 'deduction', 'benefit')
    #     def _compute_total_salary(self):
    #     for employee in self:
    #         total = employee.basic_salary + employee.allowance - employee.deduction + employee.benefit
    #         employee.total_salary = total


