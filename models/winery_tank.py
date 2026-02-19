from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WineryTank(models.Model):
    _name = 'winery.tank'
    _description = 'Tank'
    _rec_name = "name"

    name = fields.Char(string="Nombre", required = True)
    code = fields.Char(string = "Código Interno", required = True)
    _sql_constraints = [
    ("code_unique", "unique(code)", "El codigo interno debe ser único.")
    ]

    winery_tank_type_id = fields.Many2one(
    "winery.tank_type",
    string="Tipo de depósito",
    required=True
    )


    capacity_nominal = fields.Float(
    string = "Capacidad Nominal (L)",
    required = True
    )

    tolerance = fields.Float(
    string = "Tolerancia (%)"
    )

    capacity_max = fields.Float(
    string = "Capacidad Máxima Permitida (L)",
    compute = "_compute_capacity_max",
    store = True,
    readonly = True
    )

    @api.depends('capacity_nominal', 'tolerance')
    def _compute_capacity_max(self):
        for record in self:
            record.capacity_max = record.capacity_nominal + (
            record.capacity_nominal * record.tolerance / 100)

    current_liters = fields.Float(
    string = "Litros Actuales",
    default=0.0
    )

    fill_percentage = fields.Float(
    string="% de Llenado",
    compute="_compute_fill_percentage",
    store=True,
    readonly=True
    )

    @api.depends('current_liters', 'capacity_nominal')
    def _compute_fill_percentage(self):
        for record in self:
            if record.capacity_nominal > 0:
                record.fill_percentage = (
                record.current_liters / record.capacity_nominal) * 100
            else:
                record.fill_percentage = 0

    state = fields.Selection(
    [
    ('active', 'Activo'),
    ('inactive', 'Inactivo'),
    ('maintenance', 'En mantenimiento'),
    ],
    string="Estado",
    default='active'
    )

    active = fields.Boolean(default=True)

    description = fields.Text(string="Observaciones")

    @api.constrains('capacity_nominal', 'current_liters')
    def _check_positive_values(self):
        for record in self:
            if record.capacity_nominal < 0:
                raise ValidationError("La capacidad no puede ser negativa.")
            if record.current_liters < 0:
                raise ValidationError("Los litros actuales no pueden ser negativos.")