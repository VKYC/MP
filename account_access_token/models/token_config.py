from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
import random
import string

class TokenConfig(models.Model):
    _name = 'token.config'
    _description = 'Configuración de Token'

    token_size = fields.Integer(string='Tamaño del Token', default=18)
    token_duration = fields.Integer(string='Días de Duración', default=7)
    token = fields.Char(string='Token generado', compute='_compute_token', store=True, readonly=True)
    token_start_date = fields.Date(string='Fecha de inicio de validez', store=True, readonly=True)
    token_end_date = fields.Date(string='Fecha de fin de validez', store=True, readonly=True)
    name = fields.Char(string='Nombre', compute='_compute_name', store=True)

    @api.constrains('token_size')
    def _check_token_size(self):
        for record in self:
            if record.token_size < 6 or record.token_size > 18:
                raise ValidationError("El tamaño del token debe estar entre 6 y 18 dígitos.")

    @api.depends('token')
    def _compute_name(self):
        for record in self:
            record.name = record.token

    @api.model
    def create(self, vals):
        active_token = self.search([
            ('token_end_date', '>=', fields.Date.today())
        ], limit=1)
        if active_token:
            raise UserError("Ya existe un token activo. No se puede generar un nuevo token hasta que expire el actual.")
        vals['token'] = self._generate_token(vals.get('token_size', 6))
        return super(TokenConfig, self).create(vals)

    @api.depends('token_size', 'token_duration')
    def _compute_token(self):
        for record in self:
            if record.token_size and record.token_duration:
                active_token = self.env['token.config'].search([
                    ('token_end_date', '>=', fields.Date.today())
                ], limit=1)
                if not active_token:
                    token = self._generate_token(record.token_size)
                    record.token = token
                    today = fields.Date.today()
                    record.token_start_date = today
                    record.token_end_date = today + timedelta(days=record.token_duration)
                else:
                    record.token = active_token.token
                    record.token_start_date = active_token.token_start_date
                    record.token_end_date = active_token.token_end_date

    def _generate_token(self, size):
        """Genera un token aleatorio de tamaño especificado."""
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(size))