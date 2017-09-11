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
import odoo.tests.common as common


class test_partner_phonenumbers(common.SingleTransactionCase):

    @classmethod
    def setUpClass(self):
        """ I create a partner and a company. """

        super(test_partner_phonenumbers, self).setUpClass()
        res_partner = self.registry('res.partner')
        res_company = self.registry('res.company')

        cr, uid = self.cr, self.uid

        self.partner_albert_einstein = res_partner.browse(
            cr, uid, res_partner.create(cr, uid, {
                'name': 'Albert Einstein',
                'phone': '9545551234,US',
                'mobile': '7327572923,US',
                'fax': '2022684871,US'
            })
        )

        self.company_bluestar_solutions = res_company.browse(
            cr, uid, res_company.create(cr, uid, {
                'name': 'Bluestar solutions',
                'phone': '0327200890,CH',
                'fax': '0327200891,CH'
            })
        )

    @classmethod
    def tearDownClass(self):
        super(test_partner_phonenumbers, self).tearDownClass()

    def setUp(self):
        super(test_partner_phonenumbers, self).setUp()

    def tearDown(self):
        super(test_partner_phonenumbers, self).tearDown()

    def test_00_partner_phone(self):
        """ I check the stored phone is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.partner_albert_einstein.phone,
                         '+1 954-555-1234', 'Partner phone formatting failed')

    def test_10_partner_mobile(self):
        """ I check the stored mobile is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.partner_albert_einstein.mobile,
                         '+1 732-757-2923', 'Partner mobile formatting failed')

    def test_20_partner_fax(self):
        """ I check the stored fax is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.partner_albert_einstein.fax,
                         '+1 202-268-4871', 'Partner fax formatting failed')

    def test_30_company_phone(self):
        """ I check the stored phone is correctly formatted
        for fr_CH (default).
        """
        self.assertEqual(self.company_bluestar_solutions.phone,
                         '+41 32 720 08 90', 'Company phone formatting failed')

    def test_40_company_fax(self):
        """ I check the stored fax is correctly formatted
        for en_US (default).
        """
        self.assertEqual(self.company_bluestar_solutions.fax,
                         '+41 32 720 08 91', 'Company fax formatting failed')


if __name__ == '__main__':
    unittest2.main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
