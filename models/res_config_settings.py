from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    activity_days = fields.Integer("Days", config_parameter='base.activity_days', default="3")

    @api.constrains('activity_days')
    def _check_values(self):
        if self.activity_days <= 0:
            raise ValidationError('Values wrong.')
