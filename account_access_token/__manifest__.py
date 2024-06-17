{
    'name': 'Account Token Access',
    'version': '1.5.0.0.0',
    'description': 'access to accounting using a token',
    'summary': 'access to accounting using a token ',
    'author': 'Adrian Ramon Hernandez Vidrio',
    'website': 'AdrianRHV_S@outlook.com',
    'license': 'LGPL-3',
    'category': 'account',
    'depends': [
        'analytic', 'product', 'account'
    ],
    'data': [
        # 'views/account_token_view.xml',
        'security/ir.model.access.csv',
        'views/token_config_views.xml',
        'views/token_request_template.xml',
    ],
    'demo': [

    ],
    'auto_install': False,
    'application': False,
    'assets': {

    }
}