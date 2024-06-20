from odoo import _, api, fields, models
from odoo.exceptions import AccessDenied

class RequestTokenWizard(models.TransientModel):
    _name = "request.token.wizard"
    _description = "Request token wizard"

    token = fields.Char(string='Token', required=True)

    def confirm_action_journal(self):
        token_config = self.env['token.config'].search([
            ('token', '=', self.token),
            ('token_end_date', '>=', fields.Date.today())
        ], limit=1)

        if not token_config:
            raise AccessDenied(_('El token ingresado no es válido o ha expirado. Por favor, inténtelo de nuevo.'))
        action = self.env.ref('account.action_move_journal_line').read()[0]
        return action

    def confirm_action_account_moves(self):
        token_config = self.env['token.config'].search([
            ('token', '=', self.token),
            ('token_end_date', '>=', fields.Date.today())
        ], limit=1)
        if not token_config:
            raise AccessDenied(_('El token ingresado no es válido o ha expirado. Por favor, inténtelo de nuevo.'))
        action = self.env.ref('account.action_account_moves_all').read()[0]
        return action

    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}
