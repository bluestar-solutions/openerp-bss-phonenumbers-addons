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

{
    'name': 'Partner Multiple Phone Numbers',
    'version': '7.0.2.2-20160427',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Partner multiple phone numbers
==============================

With this module, the parter has a dynamic list of phone numbers, with a
category.

All existing base field (phone, mobile, fax) are synchronized with
automatically created category in both directions.

A system administrator can add custom category.
    """,
    'author': u'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['bss_partner_phonenumbers'],
    'data': ['security/ir.model.access.csv',
             'security/ir_rule.xml',

             'phone_category_data.xml',

             'phone_category_view.xml',
             'partner_view.xml', ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
