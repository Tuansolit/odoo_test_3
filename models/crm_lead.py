from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, date


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char()
    minimum_sales = fields.Float(string='Minimum Sales( before VAT)')

    def action_set_lost(self, **additional_values):
        for rec in self:
            if rec.priority == '3':
                if self.env.user.has_group('odoo_test_3.truong_phong_group_user'):
                    continue
                else:
                    raise UserError('Get the fuck out of here')
        return super(CrmLead, self).action_set_lost(**additional_values)

    def write(self, values):
        users = self.env.ref('odoo_test_3.nhan_vien_group_user').users.ids
        users1 = self.env.ref('odoo_test_3.truong_nhom_group_user').users.ids
        res = super(CrmLead, self).write(values)

        for rec in self:
            if self.env.user.id and rec.user_id.id in users:
                continue
            if self.env.user.id in users1 and rec.user_id.id in users:
                continue
            if self.env.user.id in users1 and rec.user_id.id in users1:
                continue
            else:
                raise UserError('Nope')

        return res

