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
            
        return super(HrTimeoff, self).search_read(domain, fields, offset, limit, order)
    
    def ask_approval(self):
        self.status = 'waiting'
        
    def approve(self):
        self.status = 'approved'
        
    def reject(self):
        self.status = 'rejected'
        
    def validate(self):
        attendance_obj = self.env['hr.attendance']
        attendance_ids = attendance_obj.search([('employee_id', '=', self.employee_id.id), ('plan_date', '>=', self.start_date), ('plan_date', '<=', self.end_date)])
        print(attendance_ids)
        if attendance_ids:
            for attendance in attendance_ids:
                attendance.absent_type = self.time_off_type
        else:
            attendance_obj.create({
                'employee_id': self.employee_id.id,
                'absent_type': self.time_off_type,
                'plan_date': self.start_date
            })
        self.status = 'validate'
        
    def cancel(self):
        self.status = 'cancel'
        
    def set_to_draft(self):
        self.status = 'draft'