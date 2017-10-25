# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import logging
import phonenumbers
from odoo import fields


class Phone(fields.Char):
    type = 'phone'
    _logger = logging.getLogger("Phone")

    _slots = {
        'rfc3966': 'safasdf',
    }

    def __init__(self, string=fields.Default,
                 number_type=fields.Default, **kwargs):
        super(Phone, self).__init__(
            string=string, number_type=number_type, **kwargs)

    def _parse_number(self, value):
        if not value:
            return None
        if not isinstance(value, basestring):
            value = value[0]
        if not value:
            return None
        return phonenumbers.parse(value)

    def convert_to_cache(self, value, __, validate=True):
        try:
            pn = self._parse_number(value)
            if pn:
                return (
                    phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    ).replace(' ', u'\u00A0'),
                    phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.RFC3966
                    ))
        except Exception:
            pass
#             if validate:
#                 raise ValueError("Wrong value for %s: %r" % (self, value))
        return (False, False)
