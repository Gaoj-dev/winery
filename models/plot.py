# -*- coding: utf-8 -*-

from typing import DefaultDict
from odoo import models, fields, api


class winery(models.Model):
    _name = 'winery.plot'
    _description = 'winery.plot'
    #Identificacion
    id = fields.Integer(string="ID", required=True)
    plot_number = fields.Integer(string="Numero de parcela", readonly=True, required=True)#TODO nombre de parcela se debe autogenerar
    name = fields.String(string="Nombre", required=True)
    alias = fields.String(string="Alias")
    cadastral_reference = fields.String(string="Referencia catastral")#TODO posible metodo verificar si es valido
    #Localizacion
    country = fields.Many2one( comodel_name="res.country", string="País")#TODO check no se si es res_country o res.country y falta poner el default
    province = fields.Many2one( comodel_name="res.country.province", string="Provincia") #TODO lo mismo que arriba
    locality = fields.String(string="Localidad")
    surface_ref = fields.Float(string="Superficie en hectáreas")
    #Datos vitícoras
    grape_variety = fields.Many2Many(sting="Variedad/es de la uva")
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
