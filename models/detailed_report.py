from odoo import fields, models, api
from datetime import datetime, date


class DetailedReport(models.TransientModel):
    _name = 'detailed.report'
    _description = 'Description'

    name = fields.Char()
    months = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'),
         ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')],
        default="{}".format(datetime.strftime(date.today(), '%m')))
    team_id = fields.Many2one('crm.team', string='Sales Team')

    # def _compute_set_month(self):
    #     for rec in self:
    #         rec.months = "{}".format(datetime.strftime(date.today(), '%m'))

    def action_view_report(self):
        def filter_month(f_rec):
            return f_rec.create_date.month == int(self.months)
        if not self.team_id:
            reports = self.env['crm.lead'].search([]).filtered(filter_month)
        else:
            reports = self.env['crm.lead'].search([('team_id', '=', self.team_id.id)]).filtered(filter_month)
        # plans = self.mapped('plan_id')

        action = self.env["ir.actions.actions"]._for_xml_id("odoo_test_3.odoo_test_3_report_display_action")
        if len(reports) > 1:
            action['domain'] = [('id', 'in', reports.ids)]
        elif len(reports) == 1:
            form_view = [(self.env.ref('crm.crm_lead_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = reports.id
        context = {
            'default_move_type': 'out_plan',
        }
        action['context'] = context
        return action

