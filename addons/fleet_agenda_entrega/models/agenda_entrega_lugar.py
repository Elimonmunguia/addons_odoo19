from odoo import fields, models, api


class AgendaEntregaLugar(models.Model):
    _name = "agenda.entrega.lugar"
    _description = "Lugar de la agenda de entrega"

    name = fields.Char(
        string="Nombre",
    )
    plaza = fields.Many2one(
        comodel_name="fleet.customer.plaza",
        string="Plaza",
    )