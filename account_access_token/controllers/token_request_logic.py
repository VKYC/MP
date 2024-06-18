from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError

class TokenRequestLogic(http.Controller):

    @http.route('/request_token', type='http', auth='user')
    def request_token(self, **kw):
        return request.render('account_access_token.account_token_request_template')

    @http.route('/validate_token', type='http', auth='user', methods=['POST'])
    def validate_token(self, **kw):
        token = kw.get('token')
        if token:
            valid = request.env['account.move'].check_token(token)
            if valid:
                request.session['token'] = token
                return request.redirect('/web')
        error_message = 'Invalid or expired token.'
        return request.render('account_access_token.account_token_request_template', {'error': error_message})