from odoo import _, api, fields, models
from odoo.exceptions import AccessDenied, UserError

class RequestTokenWizard(models.TransientModel):
    _name = "request.token.wizard"
    _description = "Request token wizard"

    token = fields.Char(string='Token', required=True)
    attempt_count = fields.Integer(string='contador de intentos', default=0)

    def _check_token(self, token):
        token_config = self.env['token.config'].search([
            ('token', '=', token),
            ('token_end_date', '>=', fields.Date.today())
        ], limit=1)
        return token_config

    def _increment_attempt_count(self):
        self.ensure_one()
        self.attempt_count += 1
        self.env.cr.commit()
        remaining_attempts = 3 - self.attempt_count
        if self.attempt_count >= 3:
            return True
        else:
            raise AccessDenied(_('El token ingresado no es válido o ha expirado. Le quedan %s intentos.') % remaining_attempts)

    def confirm_action_journal(self):
        self.ensure_one()
        token_config = self._check_token(self.token)
        if not token_config:
            close_window = self._increment_attempt_count()
            if close_window:
                return self.cancel()
            else:
                raise AccessDenied(_('El token ingresado no es válido o ha expirado. Por favor, inténtelo de nuevo.'))
        action = self.env.ref('account.action_move_journal_line').read()[0]
        return action

    def confirm_action_account_moves(self):
        self.ensure_one()
        token_config = self._check_token(self.token)
        if not token_config:
            close_window = self._increment_attempt_count()
            if close_window:
                return self.cancel()
            else:
                raise AccessDenied(_('El token ingresado no es válido o ha expirado. Por favor, inténtelo de nuevo.'))
        action = self.env.ref('account.action_account_moves_all').read()[0]
        return action

    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}
