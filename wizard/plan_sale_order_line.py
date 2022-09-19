from odoo import fields, models, api
from odoo.tools.translate import _


class PlanSaleOrderLine(models.Model):
    _name = 'plan.sale.order.line'
    # _inherit = 'sale.order.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('res.users')
    state_plan = fields.Selection(
        [('approved', 'Approved'),
         ('notapprove', 'NotApprove'),
         ('reject', 'Reject')],
        'State', default="notapprove")
    plan_id = fields.Many2one('plan.sale.order', string='Plan Reference', required=True, ondelete='cascade', index=True,
                              copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    check_user = fields.Boolean(compute='compute_check_user')

    def doapprove(self):
        s = 0
        self.message_post(body=_('Check it out!'),
                          # message_type='comment',
                          # subtype_xmlid='mail.mt_note',
                          )
        self.write({'state_plan': 'approved'})
        for line in self.plan_id.plan_line:
            if line.state_plan == 'reject':
                s += 1
            if line.state_plan == 'notapprove':
                s += 1
        if s == 0:
            self.plan_id.write({'state': 'approved'})
            self.plan_id.order_id.write({'state': 'sale'})
        else:
            self.plan_id.order_id.write({'state': 'draft'})
            self.plan_id.write({'state': 'process'})

    def doreject(self):
        s = 0
        self.message_post(body=_('Check it out!'),
                          # message_type='comment',
                          # subtype_xmlid='mail.mt_note',
                          )
        self.write({'state_plan': 'reject'})
        for line in self.plan_id.plan_line:
            if line.state_plan == 'approved':
                s += 1
            if line.state_plan == 'notapprove':
                s += 1
        if s == 0:
            self.plan_id.write({'state': 'reject'})
        else:
            self.plan_id.order_id.write({'state': 'draft'})
            self.plan_id.write({'state': 'process'})

    def compute_check_user(self):
        for rec in self:
            if self.env.user.id == rec.name.id:
                rec.check_user = True
            else:
                rec.check_user = False



