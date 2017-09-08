# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from odoo import models, fields


class bss_partner_multi_phone(models.Model):
    _inherit = 'res.partner'

    phone_ids = fields.one2many(
        'bss.partner.phone', 'partner_id', 'Phones', reorderable=True
    )
    phone = fields.Char(
        compute='_get_phone',
        inverse='_set_phone',
        store={
            'bss.partner.phone': (
                _get_partner_ids_by_phone_ids,
                ['number', 'category_id', 'partner_id', 'sequence'], 10
            ),
        }, multi=False, string="Phone"
    )
    fax = fields.Char(
        compute='_get_fax',
        inverse='_set_fax',
        store={
            'bss.partner.phone': (
                _get_partner_ids_by_phone_ids,
                ['number', 'category_id', 'partner_id', 'sequence'], 10
            ),
        }, multi=False, string="Fax"
    )
    mobile = fields.Char(
        compute='_get_mobile',
        inverse='_set_mobile',
        store={
            'bss.partner.phone': (
                _get_partner_ids_by_phone_ids,
                ['number', 'category_id', 'partner_id', 'sequence'], 10
            ),
        }, multi=False, string="Mobile"
    )

    @api.v7
    def _get_phone_field(self, cr, uid, ids, cat_id,
                         field_name, arg, context=None):
        phone_obj = self.pool.get('bss.partner.phone')
        result = {}
        if isinstance(ids, (int, long)):
            ids = [ids]

        # Take the first phone number by sequence for the category if exists:
        phone_ids = phone_obj.search(
            cr, uid, [('partner_id', 'in', ids),
                      ('category_id', '=', cat_id)],
            order='partner_id asc, sequence asc',
            context=context
        )
        for phone in phone_obj.browse(cr, uid, phone_ids, context):
            if phone.partner_id.id not in result.keys():
                result[phone.partner_id.id] = phone.number

        # Fill with None if the phone does not exists:
        for partner_id in list(set(ids) - set(result.keys())):
            result[partner_id] = None

        return result

    @api.v7
    def _set_phone_field(self, cr, uid, ids, cat_id,
                         name, value, context=None):
        phone_obj = self.pool.get('bss.partner.phone')

        if not value:
            return False

        if isinstance(ids, (int, long)):
            ids = [ids]

        for partner_id in ids:
            phone_ids = phone_obj.search(
                cr, uid, [('partner_id', '=', partner_id),
                          ('category_id', '=', cat_id)],
                order='partner_id asc, sequence asc',
                context=context
            )
            if phone_ids:
                phone_obj.write(cr, uid, phone_ids[0], {'number': value},
                                context)
            else:
                phone_obj.create(cr, uid, {
                    'category_id': cat_id,
                    'number': value,
                    'partner_id': partner_id,
                }, context)

        return True

    @api.v7
    def _get_phone(self, cr, uid, ids, field_name, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._get_phone_field(cr, uid, ids,
                                     cat_obj.get_category_phone_id(cr, uid),
                                     field_name, arg, context)

    @api.v7
    def _set_phone(self, cr, uid, ids, name, value, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._set_phone_field(cr, uid, ids,
                                     cat_obj.get_category_phone_id(cr, uid),
                                     name, value, context)

    @api.v7
    def _get_fax(self, cr, uid, ids, field_name, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._get_phone_field(cr, uid, ids,
                                     cat_obj.get_category_fax_id(cr, uid),
                                     field_name, arg, context)

    @api.v7
    def _set_fax(self, cr, uid, ids, name, value, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._set_phone_field(cr, uid, ids,
                                     cat_obj.get_category_fax_id(cr, uid),
                                     name, value, context)

    @api.v7
    def _get_mobile(self, cr, uid, ids, field_name, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._get_phone_field(cr, uid, ids,
                                     cat_obj.get_category_mobile_id(cr, uid),
                                     field_name, arg, context)

    @api.v7
    def _set_mobile(self, cr, uid, ids, name, value, arg, context=None):
        cat_obj = self.pool.get('bss.phone.category')
        return self._set_phone_field(cr, uid, ids,
                                     cat_obj.get_category_mobile_id(cr, uid),
                                     name, value, context)

    @api.v7
    def _get_partner_ids_by_phone_ids(self, cr, uid, ids, context=None):
        partner_ids = set()
        for phone in self.browse(cr, uid, ids, context):
            partner_ids.add(phone.partner_id.id)

        return list(partner_ids)


bss_partner_multi_phone()
