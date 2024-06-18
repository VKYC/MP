from odoo import models, fields, api
from datetime import datetime, timedelta
import random
import string

class AccountTokenConfig(models.Model):
    _name = 'account.token.config'
    _description = 'Account Token Configuration'

    name = fields.Char(string='Token', readonly=True)
    expiration_date = fields.Datetime(string='Expiration Date', readonly=True)
    token_length = fields.Integer(string='Token Length', default=0)
    duration_days = fields.Integer(string='Duration (Days)', default=0)

    @api.model
    def create_token(self):
        token_length = self.token_length
        duration_days = self.duration_days
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=token_length))
        expiration_date = datetime.now() + timedelta(days=duration_days)

        token_record = self.create({
            'name': token,
            'expiration_date': expiration_date,
        })

        return token_record

    def generate_token(self):
        self.ensure_one()
        token = self.create_token()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Token Generated',
                'message': f'Token: {token.name}',
                'sticky': False,
            }
        }
