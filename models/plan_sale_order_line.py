from odoo import fields, models, api
from odoo.tools.translate import _


class PlanSaleOrderLine(models.Model):
    _name = 'plan.sale.order.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users')
    state_plan = fields.Selection(
        [('approved', 'Approved'),
         ('not_approve', 'Not Approve'),
         ('reject', 'Reject')],
        'State', default="not_approve")
    plan_id = fields.Many2one('plan.sale.order', string='Plan Reference', required=True, ondelete='cascade', index=True,
                              copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    check_user = fields.Boolean(compute='compute_check_user')

    def do_approve(self):
        s = 0
        partner_ids = []
        partner_ids.append(self.plan_id.create_uid.partner_id.id)
        self.plan_id.message_post(body=_('Check it!'),
                                  message_type='notification',
                                  partner_ids=partner_ids
                                  )
        self.write({'state_plan': 'approved'})
        for line in self.plan_id.plan_line:
            if line.state_plan == 'reject':
                s += 1
            if line.state_plan == 'not_approve':
                s += 1
        if s == 0:
            self.plan_id.write({'state': 'approved'})
            self.plan_id.order_id.write({'state': 'sale'})
        else:
            self.plan_id.order_id.write({'state': 'draft'})
            self.plan_id.write({'state': 'process'})

    def do_reject(self):
        s = 0
        partner_ids = []
        partner_ids.append(self.plan_id.create_uid.partner_id.id)
        self.plan_id.message_post(body=_('Check it!'),
                                  message_type='notification',
                                  partner_ids=partner_ids
                                  )
        self.write({'state_plan': 'reject'})
        for line in self.plan_id.plan_line:
            if line.state_plan == 'approved':
                s += 1
            if line.state_plan == 'not_approve':
                s += 1
        if s == 0:
            self.plan_id.write({'state': 'reject'})
        else:
            self.plan_id.order_id.write({'state': 'draft'})
            self.plan_id.write({'state': 'process'})

    def compute_check_user(self):
        for rec in self:
            if self.env.user.id == rec.user_id.id:
                rec.check_user = True
            else:
                rec.check_user = False
