from odoo import fields, models, api


class FleetTramiteFleet(models.Model):
    _inherit = "fleet.vehicle"

    tramite_ids = fields.One2many(
        comodel_name='fleet.tramite',
        inverse_name='vehiculo_id',
        string='Tramites'
    )