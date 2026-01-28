# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class WineryParcel(models.Model):
    _name = 'winery.parcel'
    _description = 'Parcela Vitícola'
    _rec_name = 'name'

    code = fields.Char(string='Número de Parcela', required=True)
    
    # Nombre calculado: "Nº de parcela – Provincia – Agregado – Variedad de uva"
    name = fields.Char(
        string='Nombre de la Parcela', 
        compute='_compute_name', 
        store=True, 
        readonly=True
    )
    
    cadastral_reference = fields.Char(string='Referencia Catastral')

    # --- 2. Localización ---
    country_id = fields.Many2one(
        'res.country', 
        string='País', 
        default=lambda self: self.env.company.country_id
    )
    
    state_id = fields.Many2one(
        'res.country.state', 
        string='Provincia', 
        domain="[('country_id', '=', country_id)]"
    )
    
    city = fields.Char(string='Localidad')
    surface_area = fields.Float(string='Superficie (Ha)', digits=(16, 4))

    # --- 3. Datos Vitícolas ---
    grape_variety_id = fields.Many2one('winery.grape.variety', string='Variedad de Uva')
    
    aggregate = fields.Char(string='Agregado')
    zone = fields.Char(string='Zona')

    # --- 4. Relación con Viticultor ---
    winegrower_id = fields.Many2one('winery.winegrower', string='Viticultor', required=True)

    # --- 5. Datos Geográficos / SIGPAC ---
    gps_coordinates = fields.Char(string='Coordenadas GPS')
    sigpac_data = fields.Text(string='Información Geométrica SIGPAC')

    # --- 6. Estado y Otros ---
    state = fields.Selection([
        ('active', 'Activa'),
        ('inactive', 'Inactiva'),
        ('suspended', 'Suspendida')
    ], string='Estado', default='active', required=True)

    description = fields.Text(string='Descripción Libre')

    # --- Lógica de Negocio ---

    @api.depends('code', 'state_id', 'aggregate', 'grape_variety_id')
    def _compute_name(self):
        for record in self:
            p_code = record.code or 'Sin Nº'

            p_state = record.state_id.name if record.state_id else 'Sin Prov.'
            p_agg = record.aggregate or 'Sin Agr.'

            p_var = record.grape_variety_id.name if record.grape_variety_id else 'Sin Var.'
            
            record.name = f"{p_code} - {p_state} - {p_agg} - {p_var}"

    @api.onchange('country_id')
    def _onchange_country_id(self):
        """ Limpia la provincia si el país cambia """
        if self.country_id and self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
