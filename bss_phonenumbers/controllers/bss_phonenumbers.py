# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import logging
import phonenumbers
from odoo import http


class BssPhonenumbersController(http.Controller):

    @http.route('/bss_phonenumbers/format', type='json', auth='user')
    def format(self, number):
        if not number:
            return {'value': (None, None), 'valid': True}
        try:
            user = http.request.env.user  # @UndefinedVariable
            pn = phonenumbers.parse(number, user.company_id.country_id.code)
            return {
                'value': (
                    phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    phonenumbers.format_number(
                        pn, phonenumbers.PhoneNumberFormat.RFC3966)),
                'valid': True
            }
        except Exception:
            return {
                'value': (number, None),
                'valid': False
            }
