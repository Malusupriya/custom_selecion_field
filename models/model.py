# -*- coding: utf-8 -*-
from odoo import api, models, fields, _, tools
from odoo.addons.custom_selection_field.models.fields import Selection


class SaleOrder(models.Model):
    _inherit = "sale.order"

    custom_priority = Selection([
        ('green', 'Green', 'green'),
        ('orange', 'Orange', 'orange'),
        ('red', 'Red', 'red'),
    ], string='Priority', has_color=True)


