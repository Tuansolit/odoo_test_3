from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    plan_id = fields.Many2one('plan.sale.order', string='Business plan')
    plan_count = fields.Integer(string='Plan Count', compute='_get_planed')

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

    # def check_business_plan(self):
    #     plan_id = self.env['plan.sale.order'].search([('order_id', '=', self.id)])
    #     if not plan_id:
    #         raise ValidationError("No business plan!")

    @api.model
    def action_confirm(self):
        # self.plan_id = self.env['plan.sale.order'].search([('order_id', '=', self.id)])
        if not self.plan_id:
            raise ValidationError("No business plan!")
        if self.plan_id.order_id.id != self.id:
            raise ValidationError("Wrong plan!")
        if self.plan_id.state != 'approved':
            raise ValidationError("Plan not approved!")
        cash = super(SaleOrderInherit, self).action_confirm()

        return cash

    def action_view_plan(self):
        plans = self.env['plan.sale.order'].search([('order_id', '=', self.id)])
        # plans = self.mapped('plan_id')
        action = self.env["ir.actions.actions"]._for_xml_id("odoo_test_3.test_3_plan_display_action")
        if len(plans) > 1:
            action['domain'] = [('id', 'in', plans.ids)]
        elif len(plans) == 1:
            form_view = [(self.env.ref('odoo_test_3.test_3_plan_view_tree').id, 'tree')]
            action['domain'] = [('order_id', '=', self.id)]
            # if 'views' in action:
            #     action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            # else:
            action['views'] = form_view
            # action['res_id'] = plans.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_plan',
        }
        action['context'] = context
        return action

    def _get_planed(self):
        for order in self:
            plans = self.env['plan.sale.order'].search([('order_id', '=', self.id)])
            order.plan_count = len(plans)
