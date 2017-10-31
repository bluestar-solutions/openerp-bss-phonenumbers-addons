# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import phonenumbers
from odoo import models, api
from .. import fields
import logging


class Base(models.AbstractModel):
    _inherit = 'base'
    _phone_fields = False, []
    _logger = logging.getLogger(_inherit)

    @api.multi
    def write(self, vals):
        vals = self._process_phonenumber(vals)
        return super(Base, self).write(vals)

    @api.model
    def create(self, vals):
        vals = self._process_phonenumber(vals)
        return super(Base, self).create(vals)

    def _get_phonenumber_fields(self):
        if not self._phone_fields[0]:
            for key, field in self._fields.iteritems():
                if isinstance(field, fields.Phone):
                    self._phone_fields[1].append(key)
        return self._phone_fields[1]

    def _process_phonenumber(self, vals):
        pn_fields = self._get_phonenumber_fields()
        for field in pn_fields:
            country = self.env.user.company_id.country_id
            if country:
                country_code = country.code.upper()
            if vals.get(field):
                pn = phonenumbers.parse(vals[field], country_code)
                vals[field] = phonenumbers.format_number(
                    pn, phonenumbers.PhoneNumberFormat.E164)
        return vals
