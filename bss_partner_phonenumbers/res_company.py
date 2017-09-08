# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2016 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from odoo import models, fields
from odoo.addons.base.res.res_company import res_company


class bss_partner_phonenumbers_company(modles.Model):
    _inherit = 'res.company'

    phone = fields.Char(compute='res_company._get_address_data',
                        inverse='res_company._set_address_data',
                        size=64, string="Phone",
                        multi='address')
    fax = fields.Char(compute='res_company._get_address_data',
                      inverse='res_company._set_address_data',
                      size=64, string="Fax",
                      multi='address')


bss_partner_phonenumbers_company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
