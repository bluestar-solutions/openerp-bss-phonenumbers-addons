# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo.osv import osv
import unittest2
import odoo.tests.common as common

from odoo.addons.bss_phonenumbers import (
    bss_phonumbers_fields  # @UnresolvedImport
)


class test_phonenumbers(common.SingleTransactionCase):

    @classmethod
    def setUpClass(self):
        super(test_phonenumbers, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        super(test_phonenumbers, self).tearDownClass()

    def setUp(self):
        """ I create an array of phones. """
        super(test_phonenumbers, self).setUp()
        self.pn = bss_phonumbers_fields.phonenumber()
        self.samples = [
            '9545551234,US',
            '0411234567,CH',
            '041123456é,CH',
            '',
            '11111111111111111',
        ]

    def tearDown(self):
        super(test_phonenumbers, self).tearDown()

    def test_00_phonenumbers_formatting_en_US(self):
        """ I check the phone is correctly formatted for en_US. """
        number_phone = self.samples[0]
        res = self.pn._symbol_set_char(number_phone)
        self.assertEqual(res, '+19545551234', 'e164 phone formatting failed')
        res = self.pn._symbol_get(number_phone)
        self.assertEqual(res, '+1 954-555-1234',
                         'International phone formatting failed')

    def test_10_phonenumbers_formatting_fr_CH(self):
        """ I check the phone is correctly formatted for fr_CH. """
        number_phone = self.samples[1]
        res = self.pn._symbol_set_char(number_phone)
        self.assertEqual(res, '+41411234567', 'e164 phone formatting failed')
        res = self.pn._symbol_get(number_phone)
        self.assertEqual(res, '+41 41 123 45 67',
                         'International phone formatting failed')

    def test_20_phonenumbers_UnicodeDecodeError(self):
        """ I check invalid characters are detected. """
        number_phone = self.samples[2]
        with self.assertRaises(osv.except_osv):
            self.pn._symbol_set_char(number_phone)

    def test_30_phonenumbers_empty(self):
        """ I check the phone is correctly empty. """
        number_phone = self.samples[3]
        res = self.pn._symbol_set_char(number_phone)
        self.assertEqual(res, None, 'e164 phone formatting failed')
        res = self.pn._symbol_get(number_phone)
        self.assertEqual(res, None, 'International phone formatting failed')

    def test_40_phonenumbers_too_long(self):
        """ I check the stored phone is correctly empty. """
        number_phone = self.samples[4]
        with self.assertRaises(osv.except_osv):
            self.pn._symbol_set_char(number_phone)


if __name__ == '__main__':
    unittest2.main()
