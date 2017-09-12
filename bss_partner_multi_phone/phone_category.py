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


class communication_mode_category(models.Model):
    _name = 'bss.phone.category'
    _description = "Phone Category"

    name = fields.Char('Name', size=32, translate=True, required=True)
    required = fields.Boolean('Required', readonly=True, default=False)
    unique = fields.Boolean('Unique', readonly=True, default=False)

    @api.v7
    def _get_category_id(self, cr, uid, xml_sub_name):
        """Return the category id from the sub name of an xml id"""

        m = self.pool.get('ir.model.data')
        return m.get_object(
            cr, uid,
            'bss_partner_multi_phone',
            'phone_category_%s' % xml_sub_name
        ).id

    @api.v7
    def get_category_phone_id(self, cr, uid):
        return self._get_category_id(cr, uid, 'phone')

    @api.v7
    def get_category_fax_id(self, cr, uid):
        return self._get_category_id(cr, uid, 'fax')

    @api.v7
    def get_category_mobile_id(self, cr, uid):
        return self._get_category_id(cr, uid, 'mobile')


communication_mode_category()
