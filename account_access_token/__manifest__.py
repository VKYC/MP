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
        'security/ir.model.access.csv',
        'views/account_token_config_views.xml',
        'views/account_token_request_template.xml',
        # 'views/account_move_token_views.xml',
    ],
    'demo': [

    ],
    'auto_install': False,
    'application': False,
    'assets': {

    }
}