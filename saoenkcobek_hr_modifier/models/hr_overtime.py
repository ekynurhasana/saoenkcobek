from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrOvertime(models.Model):
    _name = 'hr.overtime'
    _description = 'HR Overtime'
    
    name = fields.Char(string='Name', copy=False)
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    attendance_id = fields.Many2one('hr.attendance', string='Attendance', required=True, domain="[('employee_id', '=', employee_id)]")
    date = fields.Date(string='Date', required=True)
    hour = fields.Float(string='Hour', required=True)
    overtime_amount = fields.Float(string='Overtime Amount', compute='_compute_overtime_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('validate', 'Validate'),
        ('cancel', 'Cancelled')],
        string='Status', default='draft')
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        user = self.env.user
        if user.has_group('saoenkcobek_hr_modifier.group_hrm_saoenkcobek_hr'):
            domain.extend([])
        elif user.has_group('saoenkcobek_hr_modifier.group_hrm_saoenkcobek_leader'):
            employee = self.env['hr.employee'].search([('parent_id', '=', user.employee_id.id)])
            domain.extend([('employee_id', 'in', employee.ids)])
        else:
            domain.extend([('employee_id', '=', user.employee_id.id)])
    
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
        
    @api.depends('hour')
    def _compute_overtime_amount(self):
        for overtime in self:
            # get max hour from res config
            max_hour = self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_maximum_hour')
            rate = self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_rate')
            hour = float(overtime.hour)
            if float(overtime.hour) > float(max_hour):
                hour = max_hour
            overtime.overtime_amount = hour * float(rate)
            
    @api.onchange('attendance_id')
    def _onchange_attendance_id(self):
        for overtime in self:
            overtime.date = overtime.attendance_id.check_in.date()
    
    
    @api.constrains('hour')
    def _check_hour(self):
        for overtime in self:
            if overtime.hour < 0:
                raise ValidationError(_('Hour must be greater than 0.0'))