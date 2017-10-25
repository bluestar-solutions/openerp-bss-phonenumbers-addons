# -*- coding: utf-8 -*-
# Part of CRM Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.addons.bss_phonenumbers import fields  # @UnresolvedImport


class Lead(models.Model):
    _inherit = 'crm.lead'

    phone = fields.Phone("Phone")
    mobile = fields.Phone("Mobile")
    fax = fields.Phone("Fax")
