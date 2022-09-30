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
    'depends': ['base', 'account', 'sale', 'sale_management', 'product', 'mail'],
    'data': ['security/ir.model.access.csv',
             'views/plan_sale_order_view.xml',
             'views/sale_order.xml',
             'views/cron_plan_sale_order.xml',
             'views/res_config_settings_view.xml'
             ],
    'demo': ['data/demo.xml'],
}
