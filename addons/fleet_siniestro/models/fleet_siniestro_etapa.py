from odoo import fields, models, api


class FleetSiniestroEtapa(models.Model):
    _name = "fleet.siniestro.etapa"
    _description = "Etapa de siniestro"

    name = fields.Char(
        string="Nombre"
    )