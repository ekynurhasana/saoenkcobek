from odoo import models, fields, api, exceptions, _

class HrPayroll(models.Model):
    _name = 'hr.payroll.template'
    _description = 'HR Payroll Template'
    
    name = fields.Char(string='Name', copy=False)
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    hr_payroll_line_ids = fields.One2many('hr.payroll.template.line', 'hr_payroll_template_id', string='Payroll Lines')
    
class HrPayrollLine(models.Model):
    _name = 'hr.payroll.template.line'
    _description = 'HR Payroll Line'
    
    name = fields.Char(string='Name')
    hr_payroll_template_id = fields.Many2one('hr.payroll.template', string='Payroll Template')
    payroll_type_id = fields.Many2one('hr.payroll.type', string='Salary Component')
    amount = fields.Float(string='Amount')
    
class HrPayrollType(models.Model):
    _name = 'hr.payroll.type'
    _description = 'HR Payroll Type'
    
    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    is_deduction = fields.Boolean(string='Is Deduction')
    is_fixed_amount = fields.Boolean(string='Is Fixed Amount')
    fixed_amount = fields.Float(string='Fixed Amount')
    
    def unlink(self):
        for payroll_type in self:
            if payroll_type.code == 'BASIC':
                raise exceptions.ValidationError(_('You cannot delete Basic Salary Component'))
        return super(HrPayrollType, self).unlink()
