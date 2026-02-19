# -*- coding: utf-8 -*-
from odoo import models, fields, api

class WineryTankType(models.Model):
    _name = 'winery.tank_type'
    _description = 'Tipo de depósito'

    name = fields.Char(string='Nombre', required = True)
    code = fields.Char(string='Código')

    material = fields.Char(string='Material')
    default_capacity = fields.Float(string='Capacidad por defecto (L)')
    default_tolerance = fields.Float(string='Tolerancia por defecto (%)')

    active = fields.Boolean(string='Activo', default=True)

    description = fields.Text(string='Descripción')