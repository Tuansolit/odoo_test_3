from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ModelName(models.Model):
    _inherit = 'crm.team'
    _description = 'Description'

    name = fields.Char()

    Jan_target = fields.Float(string='January')
    Feb_target = fields.Float(string='February')
    Mar_target = fields.Float(string='March')
    Apr_target = fields.Float(string='April')
    May_target = fields.Float(string='May')
    Jun_target = fields.Float(string='June')
    Jul_target = fields.Float(string='July')
    Aug_target = fields.Float(string='August')
    Sep_target = fields.Float(string='September')
    Oct_target = fields.Float(string='October')
    Nov_target = fields.Float(string='November')
    Dec_target = fields.Float(string='December')

    @api.constrains('jan_target', 'feb_target', 'mar_target', 'apr_target', 'may_target', 'jun_target', 'jul_target',
                    'aug_target', 'sep_target', 'oct_target', 'nov_target', 'dec_target')
    def _check_values(self):
        if self.jan_target <= 0:
            raise ValidationError('Values wrong.')
        if self.feb_target <= 0:
            raise ValidationError('Values wrong.')
        if self.mar_target <= 0:
            raise ValidationError('Values wrong.')
        if self.apr_target <= 0:
            raise ValidationError('Values wrong.')
        if self.may_target <= 0:
            raise ValidationError('Values wrong.')
        if self.jun_target <= 0:
            raise ValidationError('Values wrong.')
        if self.jul_target <= 0:
            raise ValidationError('Values wrong.')
        if self.aug_target <= 0:
            raise ValidationError('Values wrong.')
        if self.sep_target <= 0:
            raise ValidationError('Values wrong.')
        if self.oct_target <= 0:
            raise ValidationError('Values wrong.')
        if self.nov_target <= 0:
            raise ValidationError('Values wrong.')
        if self.dec_target <= 0:
            raise ValidationError('Values wrong.')
