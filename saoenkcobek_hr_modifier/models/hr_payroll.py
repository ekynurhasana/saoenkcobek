from odoo import models, fields, api, exceptions, _

class HrPayroll(models.Model):
    _name = 'hr.payroll'
    _description = 'HR Payroll'
    
    name = fields.Char(string='Name', copy=False)
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    hr_payroll_line_ids = fields.One2many('hr.payroll.line', 'hr_payroll_id', string='Payroll Lines')
    total_salary = fields.Float(string='Total Salary', compute='_compute_total_salary', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ('cancel', 'Cancelled')],
        string='Status', default='draft')
    
    def validate(self):
        self.state = 'validate'
    
    def cancel(self):
        self.state = 'cancel'
        
    
class HrPayrollLine(models.Model):
    _name = 'hr.payroll.line'
    _description = 'HR Payroll Line'
    
    name = fields.Char(string='Name')
    hr_payroll_id = fields.Many2one('hr.payroll', string='Payroll')
    payroll_type_id = fields.Many2one('hr.payroll.type', string='Salary Component')
    amount = fields.Float(string='Amount')
    sequence = fields.Integer(string='Sequence')
