from odoo import fields, models, api


class TeamSaleRp(models.TransientModel):
    _name = 'team.sale.rp'
    _description = 'Description'

    team_id = fields.Many2one('crm.team')
    sale_target = fields.Float(compute='compute_sale_target')
    actual_sale = fields.Float(compute='_compute_actual_sale')
    target_assessment_id = fields.Many2one('target.assessment.report')
    months = fields.Char()

    def _compute_actual_sale(self):
        for team in self:
            def filter_month(f_rec):
                return f_rec.create_date.strftime('%b') == team.months

            opportunity_data = self.env['crm.lead'].search(
                [('type', '=', 'opportunity'), ('team_id.id', 'in', team.team_id.mapped('id'))]).filtered(filter_month)
            if len(opportunity_data) == 0:
                team.actual_sale = 0
            else:
                for rec in opportunity_data:
                    team.actual_sale += sum(rec.order_ids.mapped('amount_untaxed'))

    @api.depends('months')
    def compute_sale_target(self):
        for rec in self:
            a = ""
            a += rec.months[0:3] + '_target'
            rec.sale_target = getattr(rec.team_id, a)
