from odoo import models, fields

class attandance(models.Model):
    _name = "attandance"
    _description = 'New Description'


    employer_name = fields.Char(string='Employer Name', required=True)
    date_attendance = fields.Date(string='Date')
    shift = fields.Char(string='Shift')
    schedule_in = fields.Datetime('schedule in', readonly=True)
    schedule_out = fields.Datetime('schedule out', readonly=True)
    attandance_status = fields.Char(string='Attendance Status')