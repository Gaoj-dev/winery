# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



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
