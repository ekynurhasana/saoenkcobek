from odoo import models, fields, api, _

class HrShift(models.Model):
    _name = 'hr.shift'
    
    name = fields.Char(string='Shift Code', required=True)
    shift_name = fields.Char(string='Shift Name', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    is_off_day = fields.Boolean(string='Is Off Day')
    