from odoo import models, fields, api, _

class CreatePayroll(models.TransientModel):
    _name = 'create.payroll'
    _description = 'Create Payroll'
    
    is_all_employee = fields.Boolean(string='All Employee', default=True)
    employee_ids = fields.Many2many('hr.employee', string='Employee')
    payroll_template_id = fields.Many2one('hr.payroll.template', string='Payroll Template')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    
    def create_payroll(self):
        if self.is_all_employee:
            employee_ids = self.env['hr.employee'].search([])
        else:
            employee_ids = self.employee_ids
        for employee in employee_ids:
            payroll = self.env['hr.payroll'].create({
                'employee_id': employee.id,
                'start_date': self.start_date,
                'end_date': self.end_date,
            })
            for payroll_template_line in self.payroll_template_id.hr_payroll_line_ids:
                amount = 0.0
                if payroll_template_line.payroll_type_id.code == 'BASIC':
                    amount = employee.basic_salary
                if payroll_template_line.amount:
                    amount = payroll_template_line.amount
                if payroll_template_line.payroll_type_id.is_fixed_amount:
                    amount = payroll_template_line.payroll_type_id.fixed_amount
                if payroll_template_line.payroll_type_id.is_deduction:
                    amount = amount * -1
                
                self.env['hr.payroll.line'].create({
                    'hr_payroll_id': payroll.id,
                    'payroll_type_id': payroll_template_line.payroll_type_id.id,
                    'amount': amount,
                })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payroll',
            'res_model': 'hr.payroll',
            'view_mode': 'tree,form',
            'domain': [('start_date', '=', self.start_date), ('end_date', '=', self.end_date)],
        }