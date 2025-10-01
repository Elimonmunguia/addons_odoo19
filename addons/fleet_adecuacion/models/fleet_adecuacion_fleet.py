from odoo import models, fields, api


class FleetAdecuacionFleet(models.Model):
    _inherit = 'fleet.vehicle'

    adecuacion_ids = fields.One2many(
        comodel_name='fleet.adecuacion',
        inverse_name='vehiculo_id',
        string='Adecuaciones'
    )