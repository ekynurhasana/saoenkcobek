from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    overtime_minimum_hour = fields.Float(string='Minimum Hour', config_parameter='saoenkcobek_hr_modifier.overtime_minimum_hour')
    overtime_maximum_hour = fields.Float(string='Maximum Hour', config_parameter='saoenkcobek_hr_modifier.overtime_maximum_hour')
    overtime_rate = fields.Float(string='Rate', config_parameter='saoenkcobek_hr_modifier.overtime_rate')
    
    late_tolerance = fields.Float(string='Late Tolerance', config_parameter='saoenkcobek_hr_modifier.late_tolerance')
    late_amount = fields.Float(string='Late Amount', config_parameter='saoenkcobek_hr_modifier.late_amount')
    
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_minimum_hour', self.overtime_minimum_hour)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_maximum_hour', self.overtime_maximum_hour)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_rate', self.overtime_rate)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.late_tolerance', self.late_tolerance)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.late_amount', self.late_amount)
        return res
        
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            overtime_minimum_hour=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_minimum_hour')),
            overtime_maximum_hour=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_maximum_hour')),
            overtime_rate=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_rate')),
            late_tolerance=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.late_tolerance')),
            late_amount=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.late_amount'))
        )
        return res
    