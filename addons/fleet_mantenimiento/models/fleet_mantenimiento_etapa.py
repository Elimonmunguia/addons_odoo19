from odoo import models, fields, api

class FleetMantenimiento(models.Model):
    _name = "fleet.mantenimiento.etapa"
    _description = "Mantenimiento de vehiculos"

    name = fields.Char(
        string="Mantenimiento"
    )