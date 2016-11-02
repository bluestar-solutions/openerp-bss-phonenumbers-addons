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

from openerp.osv import osv, fields
from openerp.addons.bss_phonenumbers \
    import bss_phonumbers_fields as pnfields  # @UnresolvedImport


class bss_partner_phone(osv.osv):

    _name = 'bss.partner.phone'
    _description = 'Partner Phone'
    _rec_name = 'number'

    _columns = {
        'number': pnfields.phonenumber('Number', required=True),
        'category_id': fields.many2one('bss.phone.category', 'Category',
                                       required=True),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        'sequence': fields.integer('Sequence', help='Gives the sequence'
                                   'order when displaying a list of phone'
                                   'numbers.'),
    }

    _order = "partner_id, sequence"

    _defaults = {
        'sequence': 10,
    }

    def _check_unique(self, cr, uid, ids, context=None):
        for phone in self.browse(cr, uid, ids, context=context):
            if phone.category_id.unique:
                cond = [('id', '!=', phone.id),
                        ('partner_id', '=', phone.partner_id.id),
                        ('category_id', '=', phone.category_id.id)]
                if self.search(cr, uid, cond, context=context, count=True):
                    return False
            return True

    _constraints = [(_check_unique, 'A unique category cannot '
                     'be used multiple times on a partner', ['category_id'])]


bss_partner_phone()
