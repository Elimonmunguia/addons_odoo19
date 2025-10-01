from  odoo import fields,models


class FacturaProductoUnspsc(models.Model):
    _inherit = 'product.unspsc.code'
    _description = 'Herencia de producto UNSPSC para añadir un campo de categoria'

    categoria_id = fields.Many2one(
        string='Categoria',
        comodel_name='producto.categoria.factura',
    )

