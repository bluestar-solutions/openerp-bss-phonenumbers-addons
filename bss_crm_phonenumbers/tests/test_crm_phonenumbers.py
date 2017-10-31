# -*- coding: utf-8 -*-
# Part of CRM Phone Numbers.
# See LICENSE file for full copyright and licensing details.

import unittest2
import odoo.tests.common as common


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
