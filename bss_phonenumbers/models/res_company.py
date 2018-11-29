# -*- coding: utf-8 -*-
# Part of Partner Phone Numbers.
# See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class Company(models.Model):
    _inherit = 'res.company'

    country_id = fields.Many2one(required=True)

    @api.model_cr
    def init(self):
        self.search([('partner_id.country_id', '=', False)]).mapped(
            'partner_id').write({'country_id': self.env.ref('base.ch').id})
