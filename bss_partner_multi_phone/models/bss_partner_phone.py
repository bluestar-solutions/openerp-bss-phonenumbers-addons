# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.addons.bss_phonenumbers import (
    fields as pnfields  # @UnresolvedImport
)


class PartnerPhone(models.Model):
    _name = 'bss.partner.phone'
    _description = 'Partner Phone'
    _rec_name = 'number'

    number = pnfields.Phone("Number", required=True)
    category_id = fields.Many2one(
        'bss.phone.category', "Category", required=True)
    partner_id = fields.Many2one('res.partner', "Partner", required=True)
    sequence = fields.Integer('Sequence', help='Gives the sequence'
                              'order when displaying a list of phone'
                              'numbers.', default=10)

    _order = "partner_id, sequence"

    @api.multi
    def _check_unique(self):
        for phone in self:
            if phone.category_id.unique:
                if self.search([
                    ('id', '!=', phone.id),
                    ('partner_id', '=', phone.partner_id.id),
                    ('category_id', '=', phone.category_id.id)
                ], count=True):
                    return False
            return True

    _constraints = [(_check_unique, 'A unique category cannot '
                     'be used multiple times on a partner', ['category_id'])]
