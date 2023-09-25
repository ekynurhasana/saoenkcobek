from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    def default_plan_check_in(self):
        start_hour = self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.working_hour_start')
        date = fields.Datetime.now()
        plan_check_in = date.replace(hour=int(start_hour), minute=0, second=0)
        return plan_check_in
    
    def default_plan_check_out(self):
        end_hour = self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.working_hour_end')
        date = fields.Datetime.now()
        plan_check_out = date.replace(hour=int(end_hour), minute=0, second=0)
        return plan_check_out
        
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=False)
    plan_check_in = fields.Datetime(string='Plan Check In', default=default_plan_check_in)
    plan_check_out = fields.Datetime(string='Plan Check Out')
    plan_date = fields.Date(string='Plan Date')
    attendance_state = fields.Selection([('draft', 'Draft'), ('checked_in', 'Checked In'), ('checked_out', 'Checked Out'), ('absent', 'Absent')], string='Attendance State', default='draft')
    absent_type = fields.Selection([('hadir', 'Hadir'), ('cuti_tahunan', 'Cuti Tahunan'), ('izin', 'Izin'), ('sakit', 'Sakit')], string='Absent Type', default='hadir')
    late = fields.Float(string='Late', compute='_compute_late')
    over_time = fields.Float(string='Over Time', compute='_compute_over_time')
    work_time_id = fields.Many2one('hr.assign.work.time', string='Work Time')
    is_request_edit = fields.Boolean(string='Is Request Edit')
    # is_approved_edit = fields.Boolean(string='Is Approved Edit')
    is_approve_edit = fields.Boolean(string='Is Approve Edit')
            
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
            
        return super(HrAttendance, self).search_read(domain, fields, offset, limit, order)
    
    def request_edit(self):
        self.is_request_edit = True
    
    def approve_edit(self):
        self.is_approve_edit = True
        self.is_request_edit = False
    
    @api.depends('check_in', 'plan_check_in')
    def _compute_late(self):
        for attendance in self:
            if attendance.check_in and attendance.plan_check_in:
                if attendance.check_in > attendance.plan_check_in:
                    attendance.late = attendance.check_in - attendance.plan_check_in
                else:
                    attendance.late = 0.0
            else:
                attendance.late = 0.0
    
    @api.depends('check_out', 'plan_check_out')
    def _compute_over_time(self):
        for attendance in self:
            if attendance.check_out and attendance.plan_check_out:
                if attendance.check_out > attendance.plan_check_out:
                    attendance.over_time = attendance.check_out - attendance.plan_check_out
                else:
                    attendance.over_time = 0.0
            else:
                attendance.over_time = 0.0
    
    def create_over_time(self):
        min_hour = self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_minimum_hour')
        print(min_hour, 'min_hour')
        overtime = self.env['hr.overtime'].search([('attendance_id', '=', self.id)])
        if overtime:
            raise exceptions.ValidationError(_("Over Time already created."))
        if float(self.over_time) > float(min_hour):
            self.env['hr.overtime'].create({
                'employee_id': self.employee_id.id,
                'attendance_id': self.id,
                'date': self.plan_date,
                'hour': self.over_time
            })
        else:
            raise exceptions.ValidationError(_("Over Time must be greater than %s hour(s).") % (min_hour))
    
    def action_view_overtime(self):
        overtime = self.env['hr.overtime'].search([('attendance_id', '=', self.id)], limit=1)
        if not overtime:
            raise exceptions.ValidationError(_("Over Time not found."))
        return {
            'name': _('Overtime'),
            'view_mode': 'form',
            'res_model': 'hr.overtime',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': [('attendance_id', '=', self.id)]
        }
    
    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check it doesn't overlap with ours
            if attendance.plan_check_in == False and attendance.plan_check_out == False:
                last_attendance_before_check_in = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '<=', attendance.check_in),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
                    raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': attendance.employee_id.name,
                        'datetime': format_datetime(self.env, attendance.check_in, dt_format=False),
                    })

                if not attendance.check_out:
                    # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
                    no_check_out_attendances = self.env['hr.attendance'].search([
                        ('employee_id', '=', attendance.employee_id.id),
                        ('check_out', '=', False),
                        ('id', '!=', attendance.id),
                    ], order='check_in desc', limit=1)
                    if no_check_out_attendances:
                        raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
                            'empl_name': attendance.employee_id.name,
                            'datetime': format_datetime(self.env, no_check_out_attendances.check_in, dt_format=False),
                        })
                else:
                    # we verify that the latest attendance with check_in time before our check_out time
                    # is the same as the one before our check_in time computed before, otherwise it overlaps
                    last_attendance_before_check_out = self.env['hr.attendance'].search([
                        ('employee_id', '=', attendance.employee_id.id),
                        ('check_in', '<', attendance.check_out),
                        ('id', '!=', attendance.id),
                    ], order='check_in desc', limit=1)
                    if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                        raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                            'empl_name': attendance.employee_id.name,
                            'datetime': format_datetime(self.env, last_attendance_before_check_out.check_in, dt_format=False),
                        })