# -*- coding: utf-8 -*-
# Part of Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import models, api


class IrFieldsConverter(models.AbstractModel):
    _inherit = 'ir.fields.converter'

    @api.model
    def _str_to_phone(self, model, field, value):
        return super(IrFieldsConverter, self)._str_to_char(model, field, value)
