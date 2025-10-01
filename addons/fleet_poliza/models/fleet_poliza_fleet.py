from odoo import models, fields, api


class FleetPolizaFleet(models.Model):
    _inherit = 'fleet.vehicle'

    poliza_ids = fields.One2many(
        comodel_name='fleet.poliza',
        inverse_name='vehiculo_id',
        string='Poliza'
    )