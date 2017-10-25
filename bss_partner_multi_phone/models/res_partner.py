# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.addons.bss_phonenumbers import (
    fields as pnfields  # @UnresolvedImport
)


class Partner(models.Model):
    _inherit = 'res.partner'

    phone_ids = fields.One2many(
        'bss.partner.phone', 'partner_id', "Phones", reorderable=True)
    phone = pnfields.Phone(
        "Phone", compute='_get_phone_numbers', inverse='_set_phone_numbers',
        store=True)
    fax = pnfields.Phone(
        "Fax", compute='_get_phone_numbers', inverse='_set_phone_numbers',
        store=True)
    mobile = pnfields.Phone(
        "Mobile", compute='_get_phone_numbers', inverse='_set_phone_numbers',
        store=True)

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
