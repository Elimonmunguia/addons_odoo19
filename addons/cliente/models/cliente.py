from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class cliente(models.Model):
    _inherit = 'res.partner'
    _description = 'Clientes'

    es_cliente = fields.Boolean(
        string='Es cliente'
    )
    fecha_nacimiento = fields.Date(
        string='Fecha de nacimiento'
    )
    genero = fields.Selection(
        string='Genero',
        selection=[
            ('M', 'Masculino'),
            ('F', 'Femenino')
        ]
    )
    curp = fields.Char(
        string='CURP'
    )
    user_landing_id = fields.Char(
        string='User Landing'
    )


    @api.model
    def create(self,vals):
        escliente = self.env.context.get('default_es_cliente')
        if escliente:
            for val in vals:
                val['customer_rank'] = 1
        res = super(cliente, self).create(vals)
        return res