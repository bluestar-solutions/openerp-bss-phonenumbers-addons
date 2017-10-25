# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.addons.bss_phonenumbers import fields  # @UnresolvedImport


class Partner(models.Model):
    _inherit = 'res.partner'

    phone = fields.Phone("Phone")
    mobile = fields.Phone("Mobile")
    fax = fields.Phone("Fax")
