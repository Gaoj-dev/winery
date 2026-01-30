# -*- coding: utf-8 -*-
from odoo import models, fields, api

# --- 3. PESADA (Weighing) ---
class WineryWeighing(models.Model):
    _name = 'winery.weighing'
    _description = 'Pesada de Entrada'

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default='Nuevo')
    date = fields.Datetime(string='Fecha y Hora', default=fields.Datetime.now)
    
    winegrower = fields.Many2one('winery.winegrower', string='Viticultor', required=True)
    winegrower_code = fields.Char(related='winegrower.code', string='Cód. Viticultor', readonly=True)

    # --- NUEVO CAMPO RELACIONAL ---
    grape_variety_id = fields.Many2one('winery.grape_variety', string='Variedad de Uva')

    plot_ids = fields.Many2many(
        'winery.parcel',
        string='Parcelas de Origen',
        domain="[('winegrower', '=', winegrower)]"
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