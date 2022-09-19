from odoo import fields, models, api
from odoo.tools.translate import _


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

    # approver_id = fields.Many2one('res.partner', string='Approver')self
    plan_line = fields.One2many('plan.sale.order.line', 'plan_id', string='Plan Lines',
                                states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                auto_join=True)

    def send_approve(self):
        self.message_post(body=_('Check it out!'),
                          message_type='comment',
                          subtype_xmlid='mail.mt_note',
                          )
        self.write({'state': 'process'})
        self.order_id.write({'plan_id': self.id})


    # @api.model
    # def create(self, vals):
    #     cashboxes = super(PlanSaleOrder, self).create(vals)
    #     self.order_id.write({'plan_id': self.id})
    #     return cashboxes
