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

import unittest2
import openerp.tests.common as common


class test_crm_phonenumbers(common.SingleTransactionCase):

    @classmethod
    def setUpClass(self):
        super(test_crm_phonenumbers, self).setUpClass()
        crm_lead = self.registry('crm.lead')

        cr, uid = self.cr, self.uid

        self.lead = crm_lead.browse(cr, uid, crm_lead.create(cr, uid, {
            'name': 'Interesting lead',
            'phone': '9545551234,US',
            'mobile': '7327572923,US',
            'fax': '2022684871,US'
        }))

    @classmethod
    def tearDownClass(self):
        super(test_crm_phonenumbers, self).tearDownClass()

    def setUp(self):
        super(test_crm_phonenumbers, self).setUp()

    def tearDown(self):
        super(test_crm_phonenumbers, self).tearDown()

    def test_00_crm_phone(self):
        """ I check the stored phone is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.lead.phone,
                         '+1 954-555-1234', 'Lead phone formatting failed')

    def test_10_crm_mobile(self):
        """ I check the stored mobile is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.lead.mobile,
                         '+1 732-757-2923', 'Lead mobile formatting failed')

    def test_20_crm_fax(self):
        """ I check the stored fax is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.lead.fax,
                         '+1 202-268-4871', 'Lead fax formatting failed')

if __name__ == '__main__':
    unittest2.main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
