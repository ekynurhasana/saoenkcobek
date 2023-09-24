from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    overtime_minimum_hour = fields.Float(string='Minimum Hour', config_parameter='saoenkcobek_hr_modifier.overtime_minimum_hour')
    overtime_maximum_hour = fields.Float(string='Maximum Hour', config_parameter='saoenkcobek_hr_modifier.overtime_maximum_hour')
    overtime_rate = fields.Float(string='Rate', config_parameter='saoenkcobek_hr_modifier.overtime_rate')
    
    
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_minimum_hour', self.overtime_minimum_hour)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_maximum_hour', self.overtime_maximum_hour)
        self.env['ir.config_parameter'].sudo().set_param('saoenkcobek_hr_modifier.overtime_rate', self.overtime_rate)
        return res
        
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            overtime_minimum_hour=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_minimum_hour')),
            overtime_maximum_hour=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_maximum_hour')),
            overtime_rate=float(self.env['ir.config_parameter'].sudo().get_param('saoenkcobek_hr_modifier.overtime_rate'))
        )
        return res
    