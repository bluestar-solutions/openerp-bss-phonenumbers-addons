# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PhoneCategory(models.Model):
    _name = 'bss.phone.category'
    _description = "Phone Category"

    name = fields.Char('Name', size=32, translate=True, required=True)
    required = fields.Boolean('Required', readonly=True)
    unique = fields.Boolean('Unique', readonly=True)

    @api.model
    def get_category_id(self, xml_sub_name):
        """Return the category id from the sub name of an xml id"""
        return self.env['ir.model.data'].get_object_reference(
            'bss_partner_multi_phone',
            'phone_category_%s' % xml_sub_name
        )[1]

    @api.model
    def get_category_phone_id(self):
        return self.get_category_id('phone')

    @api.model
    def get_category_fax_id(self, cr, uid):
        return self.get_category_id('fax')

    @api.model
    def get_category_mobile_id(self, cr, uid):
        return self.get_category_id('mobile')
