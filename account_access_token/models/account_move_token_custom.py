from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    token_id = fields.Char(string='Access Token')

    @api.model
    def check_token(self, token):
        token_record = self.env['account.token.config'].search([('name', '=', token)], limit=1)
        if token_record and token_record.expiration_date > datetime.now():
            return True
        else:
            return False

    @api.model
    def create(self, vals):
        if 'token_id' in vals:
            if not self.check_token(vals['token_id']):
                raise AccessError(_("Invalid or expired token. Access denied."))
            else:
                # Actualiza el campo name en account.token.config con el nuevo token
                token_config = self.env['account.token.config'].sudo().search([], limit=1)
                if token_config:
                    token_config.write({'name': vals['token_id']})
        else:
            raise AccessError(_("Access token required."))
        return super(AccountMove, self).create(vals)

    def write(self, vals):
        if 'token_id' in vals:
            if not self.check_token(vals['token_id']):
                raise AccessError(_("Invalid or expired token. Access denied."))
            else:
                # Actualiza el campo name en account.token.config con el nuevo token
                token_config = self.env['account.token.config'].sudo().search([], limit=1)
                if token_config:
                    token_config.write({'name': vals['token_id']})
        else:
            raise AccessError(_("Access token required."))
        return super(AccountMove, self).write(vals)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self.env.context
        token = context.get('token')
        if not token or not self.check_token(token):
            raise AccessError(_("Invalid or expired token. Access denied."))
        return super(AccountMove, self).search(args, offset, limit, order, count)