# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2016 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.bss_phonenumbers.bss_phonumbers_fields import (
    bss_phonenumbers_converter as phonumbers_converter  # @UnresolvedImport
)
import phonenumbers
import base64


class bluestar_lead_phonenumbers_failed(osv.osv_memory):

    _name = 'bss.lead.phonenumbers.failed'
    _description = 'Failed Phone Numbers'

    _columns = {
        'lead_id': fields.many2one('crm.lead', 'Lead', required=True),
        'phone': fields.char('Phone', size=64),
        'mobile': fields.char('Mobile', size=64),
        'fax': fields.char('Fax', size=64),
    }

bluestar_lead_phonenumbers_failed()


class bluestar_lead_phonenumbers_config(osv.osv_memory):

    _name = 'bss.lead.phonenumbers.config'
    _inherit = 'res.config'
    _description = 'Lead Phonenumbers Configuration'

    def default_get(self, cr, uid, fields, context=None):
        res = dict()
        if context and 'failed_ids' in context:
            CRLF = '\r\n'
            failed_obj = self.pool.get('bss.lead.phonenumbers.failed')

            res['failed_ids'] = context['failed_ids']
            res['success'] = (len(res['failed_ids']) == 0)
            res['output_file_name'] = 'failed_lead_phone_numbers.csv'

            file_content = '%s,%s,%s,%s' % (
                'Lead', 'Phone', 'Mobile', 'Fax'
            ) + CRLF
            for failed in failed_obj.browse(
                cr, uid, res['failed_ids'], context
            ):
                file_content += '%s,%s,%s,%s' % (failed.lead_id.name,
                                                 failed.phone,
                                                 failed.mobile,
                                                 failed.fax) + CRLF
            res['output_file_stream'] = base64.encodestring(file_content)

        return res

    _columns = {
        'country_id': fields.many2one('res.country', 'Default Country',
                                      required=True),
        'failed_ids': fields.many2many('bss.lead.phonenumbers.failed',
                                       'bss_lead_phonenumbers_failed_rel',
                                       'config_id', 'failed_id',
                                       'Failed Phone Numbers', readonly=True),
        'output_file_stream': fields.binary(string='Download', readonly=True),
        'output_file_name': fields.char('Filename', size=64, readonly=True),
        'success': fields.boolean('Success'),
    }

    def execute(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        failed_obj = self.pool.get('bss.lead.phonenumbers.failed')

        config = self.browse(cr, uid, ids, context)[0]

        cr.execute("SELECT id, phone, mobile, fax FROM crm_lead")
        failed_ids = []
        rows = cr.fetchall()
        for row in rows:
            lead = {'id': row[0],
                    'phone': row[1],
                    'mobile': row[2],
                    'fax': row[3]}
            failed = {}

            try:
                pn = phonumbers_converter._parse(
                    lead['phone'], config.country_id.code
                )
                if pn:
                    lead['phone'] = phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.E164
                    )
                else:
                    lead['phone'] = None
            except phonenumbers.NumberParseException:
                failed['phone'] = lead['phone']
                lead['phone'] = None
                pass
            try:
                pn = phonumbers_converter._parse(
                    lead['mobile'], config.country_id.code
                )
                if pn:
                    lead['mobile'] = phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.E164
                    )
                else:
                    lead['mobile'] = None
            except phonenumbers.NumberParseException:
                failed['mobile'] = lead['mobile']
                lead['mobile'] = None
                pass
            try:
                pn = phonumbers_converter._parse(
                    lead['fax'], config.country_id.code
                )
                if pn:
                    lead['fax'] = phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.E164
                    )
                else:
                    lead['fax'] = None
            except phonenumbers.NumberParseException:
                failed['fax'] = lead['fax']
                lead['fax'] = None
                pass

            if failed:
                failed['lead_id'] = lead['id']
                failed_ids.append(failed_obj.create(cr, uid, failed))

            cr.execute("""
                UPDATE crm_lead
                SET phone = %(phone)s,
                    mobile = %(mobile)s,
                    fax = %(fax)s
                WHERE id = %(id)s
            """, lead)

        model_data_ids = mod_obj.search(cr, uid, [
            ('model', '=', 'ir.ui.view'),
            ('name', '=', 'view_bss_lead_phonenumbers_config_failed_form')
        ], context=context)
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'],
                                   context=context)[0]['res_id']
        context.update({'failed_ids': failed_ids})
        return {
            'name': _('Migrate Lead Phone Numbers'),
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(resource_id, 'form')],
            'res_model': 'bss.lead.phonenumbers.config',
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

bluestar_lead_phonenumbers_config()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
