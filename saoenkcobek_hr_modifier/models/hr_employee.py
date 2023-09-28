from odoo import models, fields, api, exceptions, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    basic_salary = fields.Float(string='Basic Salary')
    last_attendance_id = fields.Many2one('hr.attendance', compute='_compute_last_attendance_id', store=True)
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        user = self.env.user
        if user.has_group('saoenkcobek_hr_modifier.group_hrm_saoenkcobek_hr'):
            domain.extend([])
        elif user.has_group('saoenkcobek_hr_modifier.group_hrm_saoenkcobek_leader'):
            employee = self.env['hr.employee'].search([('parent_id', '=', user.employee_id.id)])
            ids = []
            ids.extend(employee.ids)
            ids.append(user.employee_id.id)
            domain.extend([('id', 'in', ids)])
        else:
            domain.extend([('id', '=', user.employee_id.id)])
            
        return super(HrEmployee, self).search_read(domain, fields, offset, limit, order)
    
    def action_set_last_attendance(self):
        _attendance = self._compute_last_attendance_id()
        return _attendance
    
    @api.depends('attendance_ids')
    def _compute_last_attendance_id(self):
        for employee in self:
            attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('absent_type', '=', 'hadir'),
                ('attendance_state', 'in', ['checked_in', 'checked_out'])
            ], limit=1)
            employee.last_attendance_id = attendance.id
            print(employee.last_attendance_id, 'employee.last_attendance_id')
    
    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()
        date_now = fields.Date.today()
        location = self.env.context.get("attendance_location", False)
        latit = location[0]
        longit = location[1]
        if self.attendance_state != 'checked_in':
            attendance_plan = self.env['hr.attendance'].search([
                ('employee_id', '=', self.id),
                ('plan_date', '=', date_now),
                ('attendance_state', '=', 'draft'),
                ('absent_type', '=', 'hadir')], limit=1)
            if attendance_plan:
                attendance_plan.check_in = action_date
                attendance_plan.attendance_state = 'checked_in'
                if location:
                    attendance_plan.check_in_latitude = latit
                    attendance_plan.check_in_longitude = longit
                return attendance_plan
            else:
                vals = {
                    'employee_id': self.id,
                    'check_in': action_date,
                    'attendance_state': 'checked_in',
                    'plan_date': date_now,
                }
                if location:
                    vals['check_in_latitude'] = latit
                    vals['check_in_longitude'] = longit
                return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', self.id),
            ('plan_date', '=', date_now),
            ('attendance_state', '=', 'checked_in'),
            ('check_out', '=', False)
        ], limit=1)
        if attendance:
            attendance.check_out = action_date
            attendance.attendance_state = 'checked_out'
            if location:
                attendance.check_out_latitude = latit
                attendance.check_out_longitude = longit
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        employee = self.env['hr.employee'].search([('id', '=', self.id)])
        employee.action_set_last_attendance()
        return attendance