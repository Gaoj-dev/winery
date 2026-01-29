# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WineryPlot(models.Model):
    _name = 'winery.plot'
    _description = 'Parcela'
    #Identificacion
    plot_number = fields.Integer(string="Numero de parcela", required=True)
    name = fields.Char(string="Nombre", store=True, readonly=True, compute="_compute_name")
    alias = fields.Char(string="Alias")
    cadastral_reference = fields.Char(string="Referencia catastral")#TODO posible metodo verificar si es valido
    #Localizacion
    country_id = fields.Many2one('res.country', string="País", default=68)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    locality = fields.Char(string="Localidad")
    surface_ref = fields.Float(string="Superficie en hectáreas")
    #Datos vitícolas
    grape_variety_id = fields.Many2one("winery.grape_variety", string="Variedad de la uva")#Fallo de odoo
    aggregation = fields.Char()
    zone = fields.Char()

    #Datos geográficos / SIGPAC
    gps_coordinates = fields.Char(string="Coordenadas GPS")
    sigpac_info = fields.Char(string="Información geométrica SIGPAC")
    #Relacion con viticultor
    winegrower = fields.Many2one(comodel_name="winery.winegrower", string="Viticultor")#TODO tal vez hay que cambiar el nombre#Fallo de odoo

    status = fields.Selection(
        selection=[
            ('active', 'Activa'),
            ('inactive', 'Inactiva'),
            ('suspended', 'Suspendida'),
        ],
        string="Estado",
        default='active'
    )

    description = fields.Text(string="Descripcion")

    @api.depends('plot_number', 'state_id', 'aggregation', 'grape_variety_id')
    def _compute_name(self):
        for rec in self:
            parts = [
                f"Nº {rec.plot_number}" if rec.plot_number else None,
                rec.state_id.name if rec.state_id else None,
                rec.aggregation,
                rec.grape_variety_id.name if rec.grape_variety_id else None,
            ]
            rec.name = " - ".join(filter(None, parts))


    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            'domain': {
                'state_id': [('country_id', '=', self.country_id.id)]
            }
        }