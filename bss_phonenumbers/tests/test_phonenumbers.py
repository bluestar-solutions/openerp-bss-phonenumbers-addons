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
#    GNU Affero General Public License for more details.gopher
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
import unittest2
import openerp.tests.common as common

from openerp.addons.bss_phonenumbers import bss_phonumbers_fields # @UnresolvedImport
from phonenumbers import NumberParseException

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
        self.assertEqual(res, '+1 954-555-1234', 'International phone formatting failed')

    def test_10_phonenumbers_formatting_fr_CH(self):
        """ I check the phone is correctly formatted for fr_CH. """
        number_phone = self.samples[1]
        res = self.pn._symbol_set_char(number_phone)
        self.assertEqual(res, '+41411234567', 'e164 phone formatting failed')
        res = self.pn._symbol_get(number_phone)
        self.assertEqual(res, '+41 41 123 45 67', 'International phone formatting failed')

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
