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

import unittest2
import openerp.tests.common as common
from openerp.netsvc import logging


class test_partner_multi_phone(common.TransactionCase):

    @classmethod
    def setUpClass(self):
        super(test_partner_multi_phone, self).setUpClass()
        self.partner = self.registry('res.partner')
        self.phone = self.registry('bss.partner.phone')
        self.category = self.registry('bss.phone.category')
        self.phone_category_id = lambda self, cr, uid: \
            self.category.get_category_phone_id(cr, uid)
        self.fax_category_id = lambda self, cr, uid: \
            self.category.get_category_fax_id(cr, uid)
        self.mobile_category_id = lambda self, cr, uid: \
            self.category.get_category_mobile_id(cr, uid)
        self._logger = logging.getLogger(__name__)

    def setUp(self):
        super(test_partner_multi_phone, self).setUp()
        cr, uid = self.cr, self.uid

        # I create partners
        luke_id = self.partner.create(cr, uid, {
            'name': 'Luke Skywalker',
        })
        self.luke = self.partner.browse(cr, uid, luke_id)

        # I create categories
        telepathy_id = self.category.create(cr, uid, {
            'name': 'Telepathy'
        })
        self.telepathy = self.category.browse(cr, uid, telepathy_id)
        smoke_signal_id = self.category.create(cr, uid, {
            'name': 'Smoke signal'
        })
        self.smoke_signal = self.category.browse(cr, uid, smoke_signal_id)

    def test_multi_phone(self):
        """I test multiple phone numbers"""
        cr, uid = self.cr, self.uid

        self.phone.create(cr, uid, {
            'number': '+1 5550110',
            'category_id': self.phone_category_id(cr, uid),
            'partner_id': self.luke.id,
            'sequence': 10,
        })
        self.phone.create(cr, uid, {
            'number': '+1 5550105',
            'category_id': self.telepathy.id,
            'partner_id': self.luke.id,
            'sequence': 5,
        })
        self.phone.create(cr, uid, {
            'number': '+1 5550115',
            'category_id': self.smoke_signal.id,
            'partner_id': self.luke.id,
            'sequence': 15,
        })

        # Update luke
        self.luke = self.partner.browse(cr, uid, self.luke.id)

        # I check partners values
        self.assertEqual(self.luke.phone_ids[0].number, '+1 5550105')
        self.assertEqual(self.luke.phone_ids[0].category_id.name, 'Telepathy')
        self.assertEqual(self.luke.phone_ids[1].number, '+1 5550110')
        self.assertEqual(self.luke.phone_ids[1].category_id.name, 'Phone')
        self.assertEqual(self.luke.phone, '+1 5550110')  # Compatibility test
        self.assertEqual(self.luke.phone_ids[2].number, '+1 5550115')
        self.assertEqual(self.luke.phone_ids[2].category_id.name,
                         'Smoke signal')

        # I test a write
        self.phone.write(cr, uid, self.luke.phone_ids[1].id, {
            'number': '+1 5550111',
        })

        # I retrieve updated partners
        self.luke = self.partner.browse(cr, uid, self.luke.id)

        # I check partners values
        self.assertEqual(self.luke.phone_ids[1].number, '+1 5550111')
        self.assertEqual(self.luke.phone, '+1 5550111')  # Compatibility test

    def test_multi_phone_old(self):
        """I test a write by old fields for compatibility"""
        cr, uid = self.cr, self.uid

        values = {
            self.phone_category_id(cr, uid): ['+1 5550121', '+1 5550131'],
            self.fax_category_id(cr, uid): ['+1 5550122', '+1 5550132'],
            self.mobile_category_id(cr, uid): ['+1 5550123', '+1 5550133'],
        }

        # Execute test 2 times to test create and write:
        for t in [0, 1]:
            self.partner.write(cr, uid, self.luke.id, {
                'phone': values[self.phone_category_id(cr, uid)][t],
                'fax': values[self.fax_category_id(cr, uid)][t],
                'mobile': values[self.mobile_category_id(cr, uid)][t],
            })

            # Update luke
            self.luke = self.partner.browse(cr, uid, self.luke.id)

            # I check partners values
            self.assertEqual(len(self.luke.phone_ids), 3)
            for i in range(len(self.luke.phone_ids)):
                self.assertEqual(
                    self.luke.phone_ids[i].number,
                    values[self.luke.phone_ids[i].category_id.id][t]
                )
            self.assertEqual(self.luke.phone,
                             values[self.phone_category_id(cr, uid)][t])
            self.assertEqual(self.luke.fax,
                             values[self.fax_category_id(cr, uid)][t])
            self.assertEqual(self.luke.mobile,
                             values[self.mobile_category_id(cr, uid)][t])

if __name__ == '__main__':
    unittest2.main()
