from odoo import models, fields

class TokenConfig(models.Model):
    _name = 'token.config'
    _description = 'Token Configuration'

    token_length = fields.Integer(string='Token Length', default=6)
    duration_days = fields.Integer(string='Duration (Days)', default=7)

    def generate_token(self):
        self.ensure_one()
        token = self.env['account.token'].create_token()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Token Generated',
                'message': f'Token: {token}',
                'sticky': False,
            }
        }