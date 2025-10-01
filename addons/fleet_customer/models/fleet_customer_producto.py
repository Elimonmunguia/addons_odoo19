from odoo import models, fields, api

class FleetCustomerProducto(models.Model):
    _name = "fleet.customer.producto"
    _description = "Módulo personalizado para registrar los productos para los vehículos"

    name = fields.Char(
        string='Nombre de producto',
    )
    prefijo = fields.Char(
        string='Prefijo',
    )