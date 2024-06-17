from odoo import models, fields, api
import random
import string
from datetime import datetime, timedelta

class AccountToken(models.Model):
    _name = 'account.token'
    _description = 'Account Token'

    name = fields.Char(string='Token', required=True)
    expiration_date = fields.Datetime(string='Expiration Date', required=True)

    @api.model
    def create_token(self):
        config = self.env['token.config'].search([], limit=1)
        token_length = config.token_length if config else 6
        duration_days = config.duration_days if config else 7
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=token_length))
        expiration_date = datetime.now() + timedelta(days=duration_days)

        token_record = self.create({
            'name': token,
            'expiration_date': expiration_date,
        })

        return token_record