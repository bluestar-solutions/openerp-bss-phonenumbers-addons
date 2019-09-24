# -*- coding: utf-8 -*-
# Part of CRM Phone Numbers.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM Phone Numbers',
    'version': '10.0.1.1',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
CRM Phone Numbers
=================

This module replaces the phone, fax and mobile text fields of the CRM lead
by phonenumber fields from bss_phone_numbers
(https://launchpad.net/bss-phonenumbers-addons).

You can use the configuration wizard to convert all existing CRM lead phone
numbers after choosing the default country
to use for existing numbers without country code. At the end of the process,
the wizard displays a list of values that could not be interpreted.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [
        'crm',
        'bss_partner_phonenumbers',
    ],
    'data': [
        'wizard/bss_lead_update_phones_views.xml',
    ],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['images/phonenumber.png', ],
}
