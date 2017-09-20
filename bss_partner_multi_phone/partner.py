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

from odoo import models, fields, api


class bss_partner_multi_phone(models.Model):
    _inherit = 'res.partner'

    phone_ids = fields.One2many(
        'bss.partner.phone', 'partner_id', 'Phones', reorderable=True
    )
    phone = fields.Char(
        compute='_get_phone_numbers',
        inverse='_set_phone_numbers',
        store=True, string="Phone"
    )
    fax = fields.Char(
        compute='_get_phone_numbers',
        inverse='_set_phone_numbers',
        store=True, string="Fax"
    )
    mobile = fields.Char(
        compute='_get_phone_numbers',
        inverse='_set_phone_numbers',
        store=True, string="Mobile"
    )

    @api.multi
    @api.depends('phone_ids.number', 'phone_ids.category_id',
                 'phone_ids.partner_id', 'phone_ids.sequence')
    def _get_phone_numbers(self):
        cat_obj = self.env['bss.phone.category']
        fields = ['phone', 'fax', 'mobile']
        found = {cat_obj.get_category_id(f): 0 for f in fields}
        cats = {cat_obj.get_category_id(f): f for f in fields}
        for partner in self:
            found = found.fromkeys(found, 0)
            for phone in partner.phone_ids:
                if not found[phone.category_id.id]:
                    setattr(partner, cats[phone.category_id.id], phone.number)
                    found[phone.category_id.id] = 1

    @api.multi
    def _set_phone_numbers(self):
        phone_obj = self.env['bss.partner.phone']
        cat_obj = self.env['bss.phone.category']
        fields = ['phone', 'fax', 'mobile']
        found = {cat_obj.get_category_id(f): 0 for f in fields}
        cats = {cat_obj.get_category_id(f): f for f in fields}
        for partner in self:
            found = found.fromkeys(found, 0)
            for phone in partner.phone_ids:
                if not found[phone.category_id.id]:
                    phone.number = getattr(partner, cats[phone.category_id.id])
                    found[phone.category_id.id] = 1
            for cat_id, f in found.iteritems():
                number = getattr(partner, cats[cat_id])
                if not f and number:
                    phone_obj.create({
                        'category_id': cat_id,
                        'number': number,
                        'partner_id': partner.id,
                    })

bss_partner_multi_phone()
