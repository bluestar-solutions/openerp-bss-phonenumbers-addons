# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import http


class BssPhonenumbersController(http.Controller):

    @http.route('/bss_phonenumbers/country_code', type='json', auth='user')
    def country_code(self):
        user = http.request.env.user  # @UndefinedVariable
        country = user.company_id.country_id
        return country and country.code or ''
