from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class HrAssignWorkTime(models.Model):
    _name = 'hr.assign.work.time'
    _description = 'Assign Work Time'

    name = fields.Char(string='Name', required=True)
    leader_id = fields.Many2one('hr.employee', string='Leader', required=True, default=lambda self: self.env.user.employee_id)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    work_time_ids = fields.One2many('hr.assign.work.time.line', 'work_time_id', string='Work Time')
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('done', 'Done'), ('rejected', 'Rejected')], string='State', default='draft')
    
    @api.onchange('start_date', 'end_date')
    def onchange_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise UserError(_('End date cannot be set before start date.'))
            else:
                employee = self.env['hr.employee'].search([('parent_id', '=', self.leader_id.id)])
                start_date = self.start_date
                end_date = self.end_date
                for emp in employee:
                    for i in range(int((end_date - start_date).days)+1):
                            date = start_date + timedelta(days=i)
                            date = date.strftime('%Y-%m-%d')
                            self.env['hr.assign.work.time.line'].create({
                                'name': self.name,
                                'employee_id': emp.id,
                                'date': date,
                                'work_time_id': self.id
                            })
        else:
            self.work_time_ids = False
            
    def action_approved(self):
        self.state = 'approved'
    def action_rejected(self):
        self.state = 'rejected'
        
    def create_employee_attendance(self):
        if not self.work_time_ids:
            raise UserError(_('Please set the work time first.'))
        if self.state != 'approved':
            raise UserError(_('Only approved work time can be created.'))
        for line in self.work_time_ids:
            # change float to time format
            start_time = datetime.strptime(str(line.shift_id.start_time), '%H.%M')
            end_time = datetime.strptime(str(line.shift_id.end_time), '%H.%M')
            if line.shift_id:
                if line.shift_id.is_off_day == False:
                    self.env['hr.attendance'].create({
                        'employee_id': line.employee_id.id,
                        'plan_date': line.date,
                        'plan_check_in': datetime.strptime(str(line.date) + ' ' + start_time.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S'),
                        'plan_check_out': datetime.strptime(str(line.date) + ' ' + end_time.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S'),
                        'check_in': False,
                        'check_in_latitude': 0.0,
                        'check_in_longitude': 0.0,
                        'check_out_latitude': 0.0,
                        'check_out_longitude': 0.0,
                        'work_time_id': self.id
                    })
            else:
                raise UserError(_('Shift for %s is not set.') % line.employee_id.name)
        self.state = 'done'
    
class HrAssignWorkTimeLine(models.Model):
    _name = 'hr.assign.work.time.line'
    _description = 'Assign Work Time Line'
    
    name = fields.Char(string='Name', required=False)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date = fields.Date(string='Date', required=True)
    shift_id = fields.Many2one('hr.shift', string='Shift')
    work_time_id = fields.Many2one('hr.assign.work.time', string='Work Time')