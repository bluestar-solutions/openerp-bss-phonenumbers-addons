# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2013 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
    'name': 'Partner Phone Numbers',
    'version': 'master',
    "category" : 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Well formed standard phone numbers in partner form view
=======================================================

This module replaces the phone, fax and mobile text fields of the partner by phonenumber fields from bss_phone_numbers (https://launchpad.net/bss-phonenumbers-addons). 

You can use the configuration wizard to convert all existing partner phone numbers after choosing the default country 
to use for existing numbers without country code. At the end of the process, the wizard displays a list of values that could not be interpreted.    
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['base', 'bss_phonenumbers'],
    'init_xml': [],
    'update_xml': ['bss_partner_phonenumbers_partner_config_view.xml'],
    'demo_xml': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images' : ['images/phonenumber.png',],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
