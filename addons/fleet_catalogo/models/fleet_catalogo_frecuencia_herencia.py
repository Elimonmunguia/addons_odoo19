from odoo import models, fields, api

class FleetCatalogoFrecuenciaHerenciaPoliza(models.Model):
    _inherit = 'fleet.poliza'
    _description = 'Frecuencia de pago de la póliza'

    frecuencia_pago_id = fields.Many2one(
        comodel_name='fleet.catalogo.frecuencia.pago',
        string='Frecuencia de pago',
    )


class FleetCatalogoFrecuenciaHerenciaTramite(models.Model):
    _inherit = 'fleet.tramite'
    _description = 'Frecuencia de pago del tramite'

    frecuencia_pago_id = fields.Many2one(
        comodel_name='fleet.catalogo.frecuencia.pago',
        string='Frecuencia de pago',
    )