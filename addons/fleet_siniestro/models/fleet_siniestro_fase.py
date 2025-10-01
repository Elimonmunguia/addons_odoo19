from odoo import models, api, fields


class FleetSiniestroFase(models.Model):
    _name = "fleet.siniestro.fase"
    _description = "Fase de Siniestro"

    name = fields.Char(
        string="Nombre"
    )