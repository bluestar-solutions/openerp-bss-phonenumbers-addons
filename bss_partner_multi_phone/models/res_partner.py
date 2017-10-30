# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api
from odoo.addons.bss_phonenumbers import (
    fields as pnfields  # @UnresolvedImport
)


class Partner(models.Model):
    _inherit = 'res.partner'
    _logger = logging.getLogger(_inherit)

    phone_ids = fields.One2many(
        'bss.partner.phone', 'partner_id', "Phones", reorderable=True)
    phone = pnfields.Phone(
        "Phone", compute='_get_phone_numbers', inverse='_set_phone')
    fax = pnfields.Phone(
        "Fax", compute='_get_phone_numbers', inverse='_set_fax')
    mobile = pnfields.Phone(
        "Mobile", compute='_get_phone_numbers', inverse='_set_mobile')

    @api.multi
    @api.depends('phone_ids.number', 'phone_ids.category_id',
                 'phone_ids.partner_id', 'phone_ids.sequence')
    def _get_phone_numbers(self):
        cat_obj = self.env['bss.phone.category']
        fields = ['phone', 'fax', 'mobile']
        cats = {cat_obj.get_category_id(f): f for f in fields}
        for partner in self:
            found = dict.fromkeys(cats, 0)
            for phone in partner.phone_ids:
                if not found[phone.category_id.id]:
                    setattr(partner, cats[phone.category_id.id], phone.number)
                    found[phone.category_id.id] = 1

    @api.multi
    def _set_phone_numbers(self, field):
        cat_obj = self.env['bss.phone.category']
        phone_obj = self.env['bss.partner.phone']
        category_id = cat_obj.get_category_id(field)
        for partner in self:
            value = getattr(partner, field)
            found = False
            for phone in partner.phone_ids:
                if phone.category_id.id == category_id:
                    found = True
                    if value:
                        phone.number = value
                    else:
                        phone.unlink()
                    break
            if not found and value:
                if value:
                    phone_obj.create({
                        'partner_id': partner.id,
                        'category_id': category_id,
                        'number': value,
                    })

    @api.multi
    def _set_phone(self):
        self._set_phone_numbers('phone')

    @api.multi
    def _set_fax(self):
        self._set_phone_numbers('fax')

    @api.multi
    def _set_mobile(self):
        self._set_phone_numbers('mobile')
