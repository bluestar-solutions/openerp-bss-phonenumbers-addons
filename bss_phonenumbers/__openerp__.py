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

{
    'name': 'Phone Numbers',
    'version': '7.0.3.1',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Well formed standard phone numbers field
========================================

Add an ORM field type "phonenumber" which ensures that all phone numbers
will be stored in E.164 format (like "+41327200890") and displayed
in international format (like "+41 32 720 08 90") with a RFC 3966 Tel URI
(like "tel:+41-32-720-08-90"). Many formats are recognized
when the field is edited. After validation, the ORM field will transform
the entered value in E.164 format before storing it.
If you type a phone number without country code, the country set for your user
in OpenERP will be used.

The RFC 3966 Tel URI can be opened by your desktop phone application to easily
dial the number directly from an OpenERP partner form view.
With E.164 format for phone numbers in database, you can imagine server-side
features with OpenERP phone numbers and a phone server.

For phone number format transformation, the module uses python-phonenumbers
from David Drysdale (Apache License 2.0)
which have to be installed separately on your OpenERP server.
python-phonenumbers is a Python port of the Java libphonenumber library
by Google.

See bss_partner_phone_numbers and bss_crm_phone_numbers for usage.

Links
-----

* E.164 format on Wikipedia : http://en.wikipedia.org/wiki/E.164
* RFC 3966 Tel URI : http://www.ietf.org/rfc/rfc3966.txt
* python-phonenumbers : https://github.com/daviddrysdale/python-phonenumbers
* libphonenumber : https://code.google.com/p/libphonenumber
* bss_partner_phone_numbers and bss_crm_phone_numbers sources :
https://launchpad.net/bss-phonenumbers-addons
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test': [],
    'js': ['static/src/js/resource.js'],
    'qweb': ['static/src/xml/resource.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['images/phonenumber.png', ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
