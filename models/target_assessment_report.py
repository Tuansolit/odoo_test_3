from odoo import fields, models, api
from datetime import datetime


class TargetAssessmentReport(models.TransientModel):
    _name = 'target.assessment.report'
    _description = 'Description'

    name = fields.Char()
    months = fields.Selection(
        [
         ('Jan', 'January'),
         ('Feb', 'February'),
         ('Mar', 'March'),
         ('Apr', 'April'),
         ('May', 'May'),
         ('Jun', 'June'),
         ('Jul', 'July'),
         ('Aug', 'August'),
         ('Sep', 'September'),
         ('Oct', 'October'),
         ('Nov', 'November'),
         ('Dec', 'December'),
         ],
        default=datetime.today().strftime('%b'))
    team_id = fields.Many2many('crm.team', string='Sales Team')
    report_ids = fields.One2many('team.sale.rp', 'target_assessment_id')

    def action_view_report(self):
        if not self.team_id:
            self.update({'report_ids': [(0, 0, {'team_id': team.id, 'months': self.months}) for team in self.env['crm.team'].search([])]})
        else:
            self.update({'report_ids': [(0, 0, {'team_id': team.id, 'months': self.months}) for team in self.team_id]})

        action = self.env["ir.actions.actions"]._for_xml_id("odoo_test_3.team_sale_rp_act_window")
        action['res_id'] = self.id

        context = {
            'default_move_type': 'out_plan',
        }
        action['context'] = context
        return action
        # view_id = self.env.ref('odoo_test_3.team_sale_rp_tree_view').id
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Bao cao chi tiet',
        #     'view_mode': 'form',
        #     'view_id': view_id,
        #     'res_model': 'target.assessment.report',
        #     'res_id': a.id,
        #     'target': 'current',
        # }
