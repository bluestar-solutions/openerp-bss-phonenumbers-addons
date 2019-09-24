# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Phone Numbers',
    'version': '10.0.1.1',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Partner Phone Numbers
=====================

This module replaces the phone, fax and mobile text fields of the partner
by phonenumber fields from bss_phone_numbers
(https://launchpad.net/bss-phonenumbers-addons).

You can use the configuration wizard to convert all existing partner phone
numbers after choosing the default country
to use for existing numbers without country code. At the end of the process,
the wizard displays a list of values that could not be interpreted.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['bss_phonenumbers'],
    'data': [
        'wizard/bss_partner_update_phones_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['images/phonenumber.png', ],
}
