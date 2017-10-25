# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import base64
import phonenumbers
from odoo import models, fields, api
from odoo.tools.translate import _


class PartnerUpdatePhonesError(models.TransientModel):
    _name = 'bss.partner.update_phones.error'
    _description = 'Failed Phone Numbers'

    wizard_id = fields.Many2one(
        'bss.partner.update_phones', 'Wizard', required=True)
    partner_id = fields.Many2one('res.partner', "Partner", required=True)
    phone = fields.Char("Phone")
    mobile = fields.Char("Mobile")
    fax = fields.Char("Fax")


class PartnerUpdatePhones(models.TransientModel):
    _name = 'bss.partner.update_phones'
    _inherit = "res.config.installer"
    _description = "Partner Update Phones"

    country_id = fields.Many2one(
        'res.country', 'Default Country', required=True,
        default=lambda self: self.env.user.company_id.country_id.id)
    failed_ids = fields.One2many(
        'bss.partner.update_phones.error', 'wizard_id', "Errors")
    output_file_stream = fields.Binary(string='Download', readonly=True)
    output_file_name = fields.Char('Filename', size=64, readonly=True)

    def _update_number(self, partner, field, country_code):
        failed = {}
        try:
            pn = phonenumbers.parse(partner[field], country_code)
            if pn:
                partner[field] = phonenumbers.format_number(
                    pn, phonenumbers.PhoneNumberFormat.E164)
            else:
                partner[field] = None
        except Exception:
            failed[field] = partner[field]
            partner[field] = None
        return partner, failed

    @api.multi
    def execute(self):
        self.ensure_one()
        Data = self.env['ir.model.data']
        Error = self.env['bss.partner.update_phones.error']

        self._cr.execute("SELECT id, phone, mobile, fax FROM res_partner")
        for row in self._cr.fetchall():
            partner = {'id': row[0],
                       'phone': row[1],
                       'mobile': row[2],
                       'fax': row[3]}
            failed = {}
            country_code = self.country_id.code.upper()
            for field in ['phone', 'mobile', 'fax']:
                if partner[field]:
                    p, f = self._update_number(partner, field, country_code)
                    partner.update(p)
                    failed.update(f)

            self._cr.execute("""
                UPDATE res_partner
                SET phone = %(phone)s,
                    mobile = %(mobile)s,
                    fax = %(fax)s
                WHERE id = %(id)s
            """, partner)
            if failed:
                failed.update({
                    'wizard_id': self[0].id,
                    'partner_id': partner['id'],
                })
                Error.create(failed)

        wizard = self.browse(self[0].id)
        if wizard.failed_ids:
            CRLF = '\r\n'
            file_content = '%s,%s,%s,%s' % (
                "Partner", "Phone", "Mobile", "Fax"
            ) + CRLF
            for failed in wizard.failed_ids:
                file_content += '%s,%s,%s,%s' % (
                    failed.partner_id.name,
                    failed.phone or '',
                    failed.mobile or '',
                    failed.fax or '') + CRLF
            wizard.write({
                'output_file_name': 'failed_partner_phone_numbers.csv',
                'output_file_stream': base64.encodestring(file_content),
            })

        model_data = Data.search([
            ('model', '=', 'ir.ui.view'),
            ('name', '=', 'bss_partner_update_phones_form_view_failed')
        ])
        model_data.ensure_one()
        resource_id = model_data.res_id
        context = dict(self._context or {})
        return {
            'name': _('Update Partner Phones'),
            'view_mode': 'tree',
            'views': [(resource_id, 'form')],
            'res_model': 'bss.partner.update_phones',
            'res_id': wizard.id,
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
