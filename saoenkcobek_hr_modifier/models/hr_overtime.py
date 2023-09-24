from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrOvertime(models.Model):
    _name = 'hr.overtime'
    _description = 'HR Overtime'
    
    name = fields.Char(string='Name', copy=False)
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    date = fields.Date(string='Date', required=True)
    hour = fields.Float(string='Hour', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('validate', 'Validate'),
        ('cancel', 'Cancelled')],
        string='Status', default='draft')
    
    def validate(self):
        self.state = 'validate'
    
    def cancel(self):
        self.state = 'cancel'
        
    def ask_approval(self):
        self.state = 'waiting'
    
    def approve(self):
        self.state = 'approved'
        
    def reject(self):
        self.state = 'rejected'
    
    
    @api.constrains('hour')
    def _check_hour(self):
        for overtime in self:
            if overtime.hour < 0:
                raise ValidationError(_('Hour must be greater than 0.0'))