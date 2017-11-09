# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import logging
from lxml import etree
from odoo import api, fields, models
from odoo.addons.bss_phonenumbers import (
    fields as pnfields  # @UnresolvedImport
)


class Partner(models.Model):
    _inherit = 'res.partner'
    _logger = logging.getLogger(_inherit)

    phone_ids = fields.One2many(
        'bss.partner.phone', 'partner_id', "Phones", reorderable=True)
    phone = pnfields.Phone(
        "Phone", compute='_get_phone_numbers', inverse='_set_dummy',
        store=True)
    fax = pnfields.Phone(
        "Fax", compute='_get_phone_numbers', inverse='_set_dummy',
        store=True)
    mobile = pnfields.Phone(
        "Mobile", compute='_get_phone_numbers', inverse='_set_dummy',
        store=True)

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
    def _set_dummy(self):
        pass

    @api.model
    def create(self, vals):
        phone_vals = self._extract_phone_vals(vals)
        res = super(Partner, self).create(vals)
        res._set_phone_vals(phone_vals)
        return res

    @api.multi
    def write(self, vals):
        self._logger.warn(vals)
        phone_vals = self._extract_phone_vals(vals)
        super(Partner, self).write(vals)
        self._set_phone_vals(phone_vals)
        return True

    def _extract_phone_vals(self, vals):
        if 'phone_ids' in vals:
            return {}
        phone_vals = {}
        for field in ['phone', 'fax', 'mobile']:
            if field in vals:
                phone_vals[field] = vals.pop(field)
        return phone_vals

    @api.multi
    def _set_phone_vals(self, phone_vals):
        for field, value in phone_vals.iteritems():
            self._set_phone_numbers(field, value)

    @api.multi
    def _set_phone_numbers(self, field, value):
        cat_obj = self.env['bss.phone.category']
        phone_obj = self.env['bss.partner.phone']
        category_id = cat_obj.get_category_id(field)
        for partner in self:
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

    @api.model
    def fields_view_multi_phone(self, arch):
        doc = etree.fromstring(arch)
        address_nodes = doc.xpath(
            "//field[@name='street']/ancestor::group[1]")
        email_nodes = doc.xpath(
            "//field[@name='email']/ancestor::group[1]/*")
        if address_nodes and email_nodes:
            for node in email_nodes:
                address_nodes[0].append(node)
        return etree.tostring(doc)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(Partner, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            res['arch'] = self.fields_view_multi_phone(res['arch'])
        return res
