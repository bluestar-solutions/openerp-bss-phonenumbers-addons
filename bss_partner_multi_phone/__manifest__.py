# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Multiple Phone Numbers',
    'version': '10.0.1.0',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Partner Multiple Phone Numbers
==============================

With this module, the parter has a dynamic list of phone numbers, with a
category.

All existing base field (phone, mobile, fax) are synchronized with
automatically created category in both directions.

A system administrator can add custom category.
    """,
    'author': u'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [
        'bss_one2many_action',
        'bss_partner_phonenumbers',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',

        'data/phone_category_data.xml',

        'views/phone_category_views.xml',
        'views/partner_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
