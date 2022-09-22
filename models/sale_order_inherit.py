from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    plan_id = fields.Many2one('plan.sale.order', string='Business plan')


    def create_business_plan(self):
        if not self:
            return True
        view_id = self.env.ref('odoo_test_3.test_3_business_plan_form').id
        context = self._context.copy()
        return {
            'name': 'create plan',
            'view_mode': 'form',
            'res_model': 'plan.sale.order',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'default_order_id': self.id}
        }

    def check_business_plan(self):
        plan_id = self.env['plan.sale.order'].search([('order_id', '=', self.id)])
        if not plan_id:
            raise ValidationError("No business plan!")



