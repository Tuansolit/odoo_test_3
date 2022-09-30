from odoo import fields, models, api
from odoo.fields import Datetime
from odoo.tools.translate import _
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta


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
        for rec in self:
            for line in rec.plan_line:
                self.env['mail.activity'].create({
                    'summary': 'Check plan',
                    'date_deadline': date.today() + timedelta(days=int(self.env['ir.config_parameter'].get_param('base.activity_days'))),
                    'activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
                    'user_id': line.user_id.id,
                    'res_model_id': self.env['ir.model']._get_id('plan.sale.order'),
                    'res_id': rec.id
                })
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

    @api.model
    def _cron_check_plan(self):
        plans = self.env['plan.sale.order'].search([])
        for plan in plans:
            if (Datetime.today() - plan.create_date).days >= int(self.env['ir.config_parameter'].get_param('base.activity_days')):
                if plan.state == 'process' or plan.state == 'new':
                    plan.write({'state': 'reject'})

