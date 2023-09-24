from odoo import models, fields, api, _

class HrTimeoff(models.Model):
    _name = 'hr.timeoff'
    _description = 'HR Time Off'

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration = delta.days + 1
            else:
                record.duration = 0

    name = fields.Char(string='Name', required=True, copy=False)
    duration = fields.Float(string='Duration', compute='_compute_duration', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('validate', 'Validate'),
        ('cancel', 'Cancelled')],
        string='Status', default='draft')
    employee_id = fields.Many2one('hr.employee', string='Employee Name', required=True)
    time_off_type = fields.Selection([
        ('cuti_tahunan', 'Cuti Tahunan'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit')],
        string='Time Off Type', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=False)
    
    def ask_approval(self):
        self.status = 'waiting'
        
    def approve(self):
        self.status = 'approved'
        
    def reject(self):
        self.status = 'rejected'
        
    def validate(self):
        attendance_obj = self.env['hr.attendance']
        attendance_ids = attendance_obj.search([('employee_id', '=', self.employee_id.id), ('check_in', '>=', self.start_date), ('check_in', '<=', self.end_date)])
        for attendance in attendance_ids:
            attendance.absent_type = self.time_off_type
        self.status = 'validate'
        
    def cancel(self):
        self.status = 'cancel'
        
    def set_to_draft(self):
        self.status = 'draft'