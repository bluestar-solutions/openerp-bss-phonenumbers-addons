# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.addons.bss_phonenumbers import fields  # @UnresolvedImport


class Company(models.Model):
    _inherit = 'res.company'

    phone = fields.Phone(related='partner_id.phone', store=True)
    fax = fields.Phone(compute='_compute_address', inverse='_inverse_fax')
