# -*- coding: utf-8 -*-

from odoo import models, fields, api


class grape_variety(models.Model):
    _name = 'winery.grape_variety'
    _description = 'Tipo de uva'

    name = fields.Char(string="Nombre", required=True)
    color = fields.Selection(
        [
            ('tinto', 'Tinto'), 
            ('blanco', 'Blanco'), 
            ('rosado', 'Rosado'),
        ],
        string="Clasificacion",
        required=True
    )
    origin_region_id = fields.Many2one("bodega.origen", string="Region")
    is_seedless = fields.Boolean(string="Sin pepitas")
    acidity_level = fields.Float(string="Acidez")
    notes = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
