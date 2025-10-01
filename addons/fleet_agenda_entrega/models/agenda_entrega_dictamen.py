from odoo import fields, models, api


class AgendaEntregaDictamen(models.Model):
    _name = "agenda.entrega.dictamen"
    _description = "Dictamen de entrega"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = "rec_name"

    "Solicitud"
    landing_id = fields.Char(
    string="ID landing"
    )
    status_dictamen = fields.Many2one(
        comodel_name="agenda.entrega.estatus.dictamen",
        string="Estatus de dictamen"
    )
    asesor_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Asesor"
    )
    "Cliente"
    cliente = fields.Char(
        string="Cliente"
    )
    email_cliente = fields.Char(
        string="Email"
    )
    telefono_cliente = fields.Char(
        string="Telefono"
    )
    "Vehiculo"
    vehiculo_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehiculo"
    )
    numero_economico = fields.Char(
        string='N° economico',
        compute='_compute_datos_vehiculo',
        store=True
    )
    vin_sn = fields.Char(
        string='VIN',
        compute='_compute_datos_vehiculo',
        store=True
    )
    producto_id = fields.Many2one(
        comodel_name='fleet.customer.producto',
        string='Producto',
        compute='_compute_datos_vehiculo',
        store=True
    )
    plaza_id = fields.Many2one(
        comodel_name='fleet.customer.plaza',
        string='Plaza',
        compute='_compute_datos_vehiculo',
        store=True
    )
    estado_vehiculo = fields.Many2one(
        comodel_name="fleet.vehicle.state",
        string="Estado del vehiculo",
        compute='_compute_datos_vehiculo',
        store=True
    )
    rec_name = fields.Char(
        string="Nombre",
        compute='_compute_rec_name',
    )

    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for vehiculo in self:
            coche = self.env['fleet.vehicle'].browse(vehiculo.vehiculo_id.id)
            vehiculo.numero_economico = coche.numero_economico
            vehiculo.vin_sn = coche.vin_sn
            vehiculo.producto_id = coche.producto_id.id
            vehiculo.plaza_id = coche.plaza_id.id
            vehiculo.estado_vehiculo = coche.state_id.id

    @api.depends('landing_id','vin_sn','cliente')
    def _compute_rec_name(self):
        for dictamen in self:
            dictamen.rec_name = f"{dictamen.landing_id}-{dictamen.vin_sn}-{dictamen.cliente}"
