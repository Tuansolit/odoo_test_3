{
    'name': "mytest_3",
    'summary': "Manage books easily",
    'description': """
Manage Library
==============
Description related to library.
""",
    'author': "Your name",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '15.0.13.0.1.0.1',
    'depends': ['base', 'account', 'sale', 'sale_management', 'product', 'mail', 'hr', 'crm', 'sale_crm'],
    'data': ['security/ir.model.access.csv',
             'security/groups.xml',
             'security/security_rules.xml',
             'views/plan_sale_order_view.xml',
             'views/sale_order.xml',
             'views/cron_plan_sale_order.xml',
             'views/res_config_settings_view.xml',
             'data/hr_department_data.xml',
             'views/sale_team.xml',
             'views/crm_lead_views.xml',
             'views/detailed_report.xml',
             'views/team_sale_rp.xml',
             'views/target_assessment_report.xml'
             ],
    'demo': ['data/demo.xml'],
}
