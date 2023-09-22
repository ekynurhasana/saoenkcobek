from odoo import models, fields

class timeoff(models.Model):
    _name = 'timeoff'
    _description = 'izn Karyawan'

    employee_id = fields.Many2one('hr.employee', string='Employee Name', required=True)
    time_off_type = fields.Selection([
        ('paid', 'Paid Time Off'),
        ('unpaid', 'Unpaid Time Off'),
        ('sick', 'Sick Leave'),
        ('other', 'Other')],
        string='Time Off Type', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    duration = fields.Float(string='Duration', compute='_compute_duration', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')],
        string='Status', default='draft')

    # Compute the duration based on start_date and end_date
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration = delta.days + 1
            else:
                record.duration = 0