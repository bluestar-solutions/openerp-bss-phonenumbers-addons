# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-2016 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from odoo import models, fields, api
from odoo.osv import osv
from odoo.addons.base.ir.ir_fields import IrFieldsConverter
import phonenumbers


class bss_phonenumbers_converter(models.TransientModel):
    _name = 'bss.phonenumbers.converter'

    @staticmethod
    def _parse(vals, region=''):
        if isinstance(vals, dict):
            number = [vals['e164'], region]
        elif vals:
            if 'xxx' in vals:
                return vals
            number = vals.split(',')
            if len(number) == 1:
                number = [number[0], region]
        else:
            return None

        if not number[0] or number[0] == '':
            return None

        return phonenumbers.parse(*number)

    def parse(self, cr, uid, vals, context=None):
        try:
            return bss_phonenumbers_converter._parse(vals)
        except phonenumbers.NumberParseException:
            return None

    @staticmethod
    def _format(vals):
        if isinstance(vals, unicode) and vals.startswith('xxx'):
            return {
                'e164': vals,
                'international': vals,
                'rfc3966': vals,
            }

        pn = bss_phonenumbers_converter._parse(vals)
        if not pn:
            return {
                'e164': None,
                'international': None,
                'rfc3966': None,
            }
        res = {
            'e164': phonenumbers.format_number(
                pn, phonenumbers.PhoneNumberFormat.E164
            ),
            'international': phonenumbers.format_number(
                pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),
            'rfc3966': phonenumbers.format_number(
                pn, phonenumbers.PhoneNumberFormat.RFC3966
            ),
        }

        # Format +32XXXXXXXXX Belgian numbers according to test in portal_crm
        # (which will succeed with this format) :
        if res['e164'][:3] == '+32' and len(res['e164']) == 12:
            res['international'] = '%s %s %s %s %s' % (
                res['e164'][:3], res['e164'][3:6], res['e164'][6:8],
                res['e164'][8:10], res['e164'][10:12]
            )
        return res

    @api.v7
    def format(self, cr, uid, number, context=None):
        try:
            return bss_phonenumbers_converter._format(number)
        except phonenumbers.NumberParseException:
            return {
                'e164': None,
                'international': None,
                'rfc3966': None,
            }


bss_phonenumbers_converter()


class Phonenumber(fields.Char):
    _type = 'phonenumber'

    def __init__(self, string="unknown", **args):
        fields.Char.__init__(self, string=string, size=64, **args)
        # TODO: Does not work in Odoo 10.o
        # self._symbol_f = self._symbol_set_char = lambda x:
        #     self._format_vals(x)
        # self._symbol_set = (super(Phonenumber, self).
        #     _symbol_c, self._symbol_f)

    def _format_vals(self, vals):
        try:
            res = bss_phonenumbers_converter._format(vals)
        except phonenumbers.NumberParseException:
            raise osv.except_osv(
                'Error', 'Invalid phone number for field : %s' % self.string
            )
        except UnicodeDecodeError:
            raise osv.except_osv(
                'Error', 'Invalid characters used for field : %s' % self.string
            )

        return res['e164']

    def _symbol_get(self, number):
        result = {}
        if number:
            pn = bss_phonenumbers_converter._format(number)
            result = pn['international']
        else:
            result = None
        return result


class pn_fields_converter(IrFieldsConverter):

    def _str_to_phonenumber(self, cr, uid, model, column, value, context=None):
        return super(pn_fields_converter, self)._str_to_char(
            cr, uid, model, column, value, context
        )
