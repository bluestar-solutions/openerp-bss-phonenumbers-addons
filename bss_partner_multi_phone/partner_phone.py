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
from odoo.addons.bss_phonenumbers \
    import bss_phonumbers_fields as pnfields  # @UnresolvedImport


class bss_partner_phone(models.Model):
    _name = 'bss.partner.phone'
    _description = 'Partner Phone'
    _rec_name = 'number'

    number = pnfields.Phonenumber('Number', required=True)
    category_id = fields.Many2one('bss.phone.category', 'Category',
                                  required=True)
    partner_id = fields.Many2one('res.partner', 'Partner')
    sequence = fields.Integer('Sequence', help='Gives the sequence'
                              'order when displaying a list of phone'
                              'numbers.', default=10)

    _order = "partner_id, sequence"

    @api.multi
    def _check_unique(self):
        for phone in self:
            if phone.category_id.unique:
                if self.search([
                    ('id', '!=', phone.id),
                    ('partner_id', '=', phone.partner_id.id),
                    ('category_id', '=', phone.category_id.id)
                ], count=True):
                    return False
            return True

    _constraints = [(_check_unique, 'A unique category cannot '
                     'be used multiple times on a partner', ['category_id'])]


bss_partner_phone()
