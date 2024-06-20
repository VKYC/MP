from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
import random
import string
import logging

# _logger = logging.getLogger(__name__) solo debug

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
        new_record = super(TokenConfig, self).create(vals)
        self._send_notification_and_email(new_record)
        return new_record

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

    def _send_notification_and_email(self, record):
        """Envía notificaciones y correos electrónicos a las personas adecuadas."""
        job_titles = ['Gerente de administracion y finanzas', 'subgerente de administracion y finanzas']
        employees = self.env['hr.employee'].search([
            '|',
            ('job_id.name', 'ilike', job_titles[0]),
            ('job_id.name', 'ilike', job_titles[1])
        ])

        # _logger.info(f"Found {len(employees)} employees matching the criteria")

        for employee in employees:
            # _logger.info(f"Processing employee {employee.name} with email {employee.work_email}")
            if employee.work_email:
                self._send_email(employee.work_email, record)

    def _send_email(self, email, record):
        """Envía un correo electrónico con la información del token."""
        mail_values = {
            'subject': f'Token Generado: {record.token}',
            'body_html': f"""
                <p>Se ha generado un nuevo token.</p>
                <p><strong>Token:</strong> {record.token}</p>
                <p><strong>Fecha de inicio:</strong> {record.token_start_date}</p>
                <p><strong>Fecha de vencimiento:</strong> {record.token_end_date}</p>
            """,
            'email_from': self.env.user.email,
            'email_to': email,
        }
        mail = self.env['mail.mail'].create(mail_values)
        # _logger.info(f"Mail created: {mail_values}")
        mail.send()
        # _logger.info(f"Mail sent to {email}")
