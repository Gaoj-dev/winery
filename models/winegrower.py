# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# ---------------------------------------------------------

class WineryWinegrower(models.Model):
    _name = "winery.winegrower"
    _description = "Winegrower"
    _rec_name = "name"

    # --------------------
    # General data
    # --------------------
    name = fields.Char(
        string="Name / Business name",
        required=True
    )
    vat = fields.Char(
        string="VAT / Tax ID"
    )
    code = fields.Char(
        string="Internal Code",
        required=True,
        copy=False
    )

    # --------------------
    # Address
    # --------------------
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip = fields.Char(string="ZIP")

    country_id = fields.Many2one(
        "res.country",
        string="Country",
        default=lambda self: self.env.company.country_id.id,
        required=True
    )

    state_id = fields.Many2one(
        "res.country.state",
        string="State / Province",
        domain="[('country_id', '=', country_id)]"
    )

    # --------------------
    # Contact
    # --------------------
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    # --------------------
    # Other
    # --------------------
    description = fields.Text(string="Notes")


    # 1. Relación One2many con 'Plot' (Parcelas)
    plot_ids = fields.One2many(
        comodel_name="winery.plot",
        inverse_name="winegrower",
        string="Vineyard Plots"
    )

    # 2. Superficie total calculada (Suma de surface_ha)
    total_surface_ha = fields.Float(
        string="Total Surface (ha)",
        compute="_compute_classification_and_surface",
        store=True
    )

    # 3. Clasificación automática (Pequeño, Mediano, Grande)
    winegrower_type = fields.Selection(
        selection=[
            ('small', 'Pequeño Viticultor (< 5 ha)'),
            ('medium', 'Mediano Viticultor (5 - 20 ha)'),
            ('large', 'Gran Viticultor (>= 20 ha)')
        ],
        string="Classification",
        compute="_compute_classification_and_surface",
        store=True
    )

    # --------------------
    # Compute Methods
    # --------------------
    @api.depends('plot_ids', 'plot_ids.surface_ha')
    def _compute_classification_and_surface(self):
        for record in self:
            # Sumamos el campo 'surface_ha' de los plots relacionados
            total_ha = sum(plot.surface_ha for plot in record.plot_ids)
            record.total_surface_ha = total_ha

            # Lógica de clasificación
            if total_ha < 5:
                record.winegrower_type = 'small'
            elif 5 <= total_ha < 20:
                record.winegrower_type = 'medium'
            else:
                record.winegrower_type = 'large'

    # --------------------
    # SQL constraints
    # --------------------
    _sql_constraints = [
        (
            "winery_winegrower_code_unique",
            "unique(code)",
            "Internal Code must be unique."
        )
    ]

    # --------------------
    # Onchange
    # --------------------
    @api.onchange("country_id")
    def _onchange_country_id(self):
        if self.state_id and self.country_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            "domain": {
                "state_id": [
                    ("country_id", "=", self.country_id.id if self.country_id else False)
                ]
            }
        }

    # --------------------
    # Validations
    # --------------------
    @api.constrains("email")
    def _check_email_format(self):
        for rec in self:
            if rec.email and "@" not in rec.email:
                raise ValidationError(
                    _("Please provide a valid email address.")
                )
