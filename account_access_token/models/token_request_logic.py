from odoo import http
from odoo.http import request

class TokenRequestLogic(http.Controller):

    @http.route('/request_token', type='http', auth='user')
    def request_token(self, **kw):
        return request.render('my_module.token_request_form')

    @http.route('/validate_token', type='http', auth='user', methods=['POST'])
    def validate_token(self, **kw):
        token = kw.get('token')
        valid = request.env['account.move'].check_token(token)
        if valid:
            request.session['token'] = token
            return request.redirect('/web')
        else:
            return request.render('my_module.token_request_form', {'error': 'Invalid or expired token.'})

