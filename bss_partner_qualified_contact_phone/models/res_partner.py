# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.addons.bss_phonenumbers import fields  # @UnresolvedImport


class PartnerQualifiedContactRel(models.Model):
    _inherit = 'bss.partner.qualified_contact.rel'

    phone = fields.Phone("Phone", related='contact_id.phone', readonly=True)
    mobile = fields.Phone(
        string="Mobile", related='contact_id.mobile', readonly=True)
