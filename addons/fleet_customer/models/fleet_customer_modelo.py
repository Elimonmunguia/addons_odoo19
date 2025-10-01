from odoo import models, fields, api


class FleetCustomerModelo(models.Model):
    _inherit = 'fleet.vehicle.model'

    prefijo = fields.Char(
        string='Prefijo'
    )