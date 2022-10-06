from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class PlanSaleOrderLine(models.Model):
    _name = 'plan.sale.order.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users')
    state_plan = fields.Selection(
        [('approved', 'Approved'),
         ('not_approve', 'Not Approve'),
         ('reject', 'Reject')],
        'State', default="not_approve")
    plan_id = fields.Many2one('plan.sale.order', string='Plan Reference', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    check_user = fields.Boolean(compute='compute_check_user')

    def do_approve(self):
        partner_ids = []
        partner_ids.append(self.plan_id.create_uid.partner_id.id)
        self.plan_id.message_post(body=_(str(self.user_id.name) + ' approved plan!'),
                                  message_type='notification',
                                  partner_ids=partner_ids
                                  )
        self.write({'state_plan': 'approved'})
        x = True
        for line in self.plan_id.plan_line:
            if line.state_plan == 'reject' or line.state_plan == 'not_approve':
                self.plan_id.order_id.write({'state': 'draft'})
                self.plan_id.write({'state': 'process'})
                x = False
                break
        if x:
            self.plan_id.write({'state': 'approved'})
            self.plan_id.order_id._action_confirm()
        # for line in self.plan_id.plan_line:
        #     if line.state_plan == 'reject':
        #         s += 1
        #     if line.state_plan == 'not_approve':
        #         s += 1
        # if s == 0:
        #     self.plan_id.write({'state': 'approved'})
        #     self.plan_id.order_id.write({'state': 'sale'})
        # else:
        #     self.plan_id.order_id.write({'state': 'draft'})
        #     self.plan_id.write({'state': 'process'})

    def do_reject(self):
        partner_ids = []
        partner_ids.append(self.plan_id.create_uid.partner_id.id)
        self.plan_id.message_post(body=_(str(self.user_id.name) + ' reject plan!'),
                                  message_type='notification',
                                  partner_ids=partner_ids
                                  )
        self.write({'state_plan': 'reject'})
        x = True
        for line in self.plan_id.plan_line:
            if line.state_plan == 'approved' or line.state_plan == 'not_approve':
                self.plan_id.order_id.write({'state': 'draft'})
                self.plan_id.write({'state': 'process'})
                x = False
                break
        if x:
            self.plan_id.write({'state': 'reject'})
            # self.plan_id.order_id.write({'state': 'draft'})

    def compute_check_user(self):
        for rec in self:
            if self.env.user.id == rec.user_id.id:
                rec.check_user = True
            else:
                rec.check_user = False

    def unlink(self):
        if self.env.user.id != self.plan_id.create_uid.id:
            raise UserError("Can't delete")
        return super(PlanSaleOrderLine, self).unlink()

    @api.model
    def create(self, vals):
        res = super(PlanSaleOrderLine, self).create(vals)
        if res.plan_id:
            if self.env.user.id != res.plan_id.create_uid.id:
                raise UserError("Can't create")
        return res
