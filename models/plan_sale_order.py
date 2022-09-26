from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _description = 'Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    order_id = fields.Many2one('sale.order', readonly=True)
    business_plan_info = fields.Char(required=True)
    state = fields.Selection(
        [('new', 'New'),
         ('process', 'Process'),
         ('approved', 'Approved'),
         ('reject', 'Reject')],
        'State', default="new")
    plan_line = fields.One2many('plan.sale.order.line', 'plan_id', string='Plan Lines')

    def send_approve(self):
        partner_ids = []
        for line in self.plan_line:
            partner_ids.append(line.user_id.partner_id.id)
        self.message_post(
            body=_(str(self.create_uid.name) + ' demand you to see and respond order plan ' + str(self.order_id.name)),
            message_type='notification',
            partner_ids=partner_ids
        )
        self.write({'state': 'process'})
        self.order_id.write({'plan_id': self.id})

    def write(self, values):
        for rec in self:
            if self.env.user.id != rec.create_uid.id:
                if 'name' in values:
                    raise UserError('You are not allowed to modify ''name and business_plan_info')
                if 'business_plan_info' in values:
                    raise UserError('You are not allowed to modify ''name and business_plan_info')
        return super(PlanSaleOrder, self).write(values)
