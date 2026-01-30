# -*- coding: utf-8 -*-
from odoo import models, fields, api

# --- CLASE AUXILIAR (Variedad de Uva) ---
class WineryGrapeVariety(models.Model):
    _name = 'winery.grape_variety'
    _description = 'Variedad de Uva'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código')

# --- 1. VITICULTOR ---
class WineryWinegrower(models.Model):
    _name = 'winery.winegrower'
    _description = 'Viticultor'
    _rec_name = 'name'

    name = fields.Char(string='Nombre Completo', required=True)
    vat = fields.Char(string='NIF/CIF')
    code = fields.Char(string='Código Interno', required=True)
    street = fields.Char(string='Dirección')
    city = fields.Char(string='Ciudad')
    zip = fields.Char(string='Código Postal')
    phone = fields.Char(string='Teléfono')
    email = fields.Char(string='Email')
    description = fields.Text(string='Notas')

    parcel_ids = fields.One2many('winery.parcel', 'winegrower_id', string='Parcelas')

# --- 2. PARCELA ---
class WineryParcel(models.Model):
    _name = 'winery.parcel'
    _description = 'Parcela'
    _rec_name = 'name'

    code = fields.Char(string='Código Polígono/Parcela', required=True)
    cadastral_reference = fields.Char(string='Ref. Catastral')
    city = fields.Char(string='Localidad')
    surface_area = fields.Float(string='Superficie (ha)')
    aggregate = fields.Char(string='Agregado')
    zone = fields.Char(string='Paraje/Zona')
    gps_coordinates = fields.Char(string='Coordenadas GPS')
    sigpac_data = fields.Text(string='Datos SIGPAC')
    state = fields.Selection([
        ('active', 'Activa'),
        ('inactive', 'Inactiva')
    ], string='Estado', default='active')
    description = fields.Text(string='Descripción')

    winegrower_id = fields.Many2one('winery.winegrower', string='Viticultor', required=True)
    grape_variety_id = fields.Many2one('winery.grape_variety', string='Variedad de Uva')

    name = fields.Char(string='Nombre', compute='_compute_name', store=True)

    @api.depends('code', 'city')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.code} - {record.city or ''}"

# --- 3. PESADA (Weighing) ---
class WineryWeighing(models.Model):
    _name = 'winery.weighing'
    _description = 'Pesada de Entrada'

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default='Nuevo')
    date = fields.Datetime(string='Fecha y Hora', default=fields.Datetime.now)
    
    winegrower_id = fields.Many2one('winery.winegrower', string='Viticultor', required=True)
    winegrower_code = fields.Char(related='winegrower_id.code', string='Cód. Viticultor', readonly=True)

    # --- NUEVO CAMPO RELACIONAL ---
    grape_variety_id = fields.Many2one('winery.grape_variety', string='Variedad de Uva')

    parcel_ids = fields.Many2many(
        'winery.parcel',
        string='Parcelas de Origen',
        domain="[('winegrower_id', '=', winegrower_id)]"
    )

    is_table_wine = fields.Boolean(string='Es Vino de Mesa')
    alcohol_degree = fields.Float(string='Graduación Alcohólica')

    gross_weight = fields.Float(string='Peso Bruto (Kg)')
    tare_weight = fields.Float(string='Tara (Kg)')
    net_weight = fields.Float(string='Peso Neto (Kg)', compute='_compute_net_weight', store=True)

    # --- CAMPO DESCRIPCIÓN ---
    description = fields.Text(string='Observaciones')

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for record in self:
            record.net_weight = record.gross_weight - record.tare_weight

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('winery.weighing') or 'Nuevo'
        return super(WineryWeighing, self).create(vals)