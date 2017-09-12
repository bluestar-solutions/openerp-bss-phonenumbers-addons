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

from odoo import models
from odoo.addons.bss_phonenumbers import (
    bss_phonumbers_fields as pnfields  # @UnresolvedImport
)


class bss_partner_phonenumbers_partner(models.Model):
    _inherit = 'res.partner'

    phone = pnfields.Phonenumber('Phone')
    mobile = pnfields.Phonenumber('Mobile')
    fax = pnfields.Phonenumber('Fax')

bss_partner_phonenumbers_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
