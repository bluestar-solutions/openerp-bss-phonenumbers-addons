# -*- coding: utf-8 -*-
from openerp.osv import osv
import unittest2
import openerp.tests.common as common
 
class test_partner_phonenumbers(common.SingleTransactionCase):
     
    @classmethod
    def setUpClass(self):
        """ I create a partner and a company. """

        super(test_partner_phonenumbers,self).setUpClass()
        res_partner = self.registry('res.partner')
        res_company = self.registry('res.company')
        
        cr, uid = self.cr, self.uid
        
        self.partner_albert_einstein = res_partner.browse(cr, uid, res_partner.create(cr, uid,
             {'name': 'Albert Einstein',
              'phone': '9545551234,US',
              'mobile': '7327572923,US',
              'fax': '2022684871,US'
              }))
        
        self.company_bluestar_solutions = res_company.browse(cr, uid, res_company.create(cr, uid,
             {'name': 'Bluestar solutions',
              'phone': '0327200890,CH',
              'fax': '0327200891,CH'
              }))
        
    @classmethod
    def tearDownClass(self):
        super(test_partner_phonenumbers,self).tearDownClass()
     
    def setUp(self):
        super(test_partner_phonenumbers,self).setUp()
         
    def tearDown(self):
        super(test_partner_phonenumbers,self).tearDown()

    def test_00_partner_phone(self):
        """ I check the stored phone is correctly formatted for en_US (default). """
        self.assertEqual(self.partner_albert_einstein.phone, '+1 954-555-1234', 'Partner phone formatting failed')
        
    def test_10_partner_mobile(self):
        """ I check the stored mobile is correctly formatted for en_US (default). """
        self.assertEqual(self.partner_albert_einstein.mobile, '+1 732-757-2923', 'Partner mobile formatting failed')
        
    def test_20_partner_fax(self):
        """ I check the stored fax is correctly formatted for en_US (default). """
        self.assertEqual(self.partner_albert_einstein.fax, '+1 202-268-4871', 'Partner fax formatting failed')
        
    def test_30_company_phone(self):
        """ I check the stored phone is correctly formatted for fr_CH (default). """
        self.assertEqual(self.company_bluestar_solutions.phone, '+41 32 720 08 90', 'Company phone formatting failed')
        
    def test_40_company_fax(self):
        """ I check the stored fax is correctly formatted for en_US (default). """
        self.assertEqual(self.company_bluestar_solutions.fax, '+41 32 720 08 91', 'Company fax formatting failed')

if __name__ == '__main__':
    unittest2.main()