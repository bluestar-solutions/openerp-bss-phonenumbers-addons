# -*- coding: utf-8 -*-
# Part of Partner Multiple Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.addons.bss_phonenumbers import (
    fields as pnfields  # @UnresolvedImport
)


class PartnerPhone(models.Model):
    _name = 'bss.partner.phone'
    _description = 'Partner Phone'
    _rec_name = 'number'
    _order = "partner_id, sequence"

    number = pnfields.Phone("Number", required=True)
    category_id = fields.Many2one(
        'bss.phone.category', "Category", required=True)
    partner_id = fields.Many2one(
        'res.partner', "Partner", required=True, ondelete='cascade')
    sequence = fields.Integer(
        'Sequence', help='Gives the sequence order when displaying '
        'a list of phone numbers.', default=10)

    @api.constrains('category_id')
    def _check_unique(self):
        if self.category_id.unique and self.search([
            ('id', '!=', self.id),
            ('partner_id', '=', self.partner_id.id),
            ('category_id', '=', self.category_id.id)
        ], count=True):
            raise ValidationError(_(
                "A unique category cannot be used multiple times "
                "on a partner."))
