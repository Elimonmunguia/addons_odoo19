from odoo import models, fields, api


class FleetSiniestro(models.Model):
    _name = 'fleet.siniestro'
    _description = 'Siniestro'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rec_name'


    etapa_id = fields.Many2one(
        comodel_name='fleet.siniestro.etapa',
        string='Etapa',
        tracking=True,
    )
    fase_id = fields.Many2one(
        comodel_name='fleet.siniestro.fase',
        string='Fase',
        tracking=True,
    )
    aseguradora_id = fields.Many2one(
        comodel_name='res.partner',
        string='Aseguradora',
    )
    siniestro_tipo_id = fields.Many2one(
        comodel_name='fleet.siniestro.tipo',
        string='Tipo de siniestro',
        tracking=True,
    )
    movilidad_id = fields.Many2one(
        comodel_name='fleet.siniestro.movilidad',
        string='Movilidad',
        tracking=True,
    )
    folio = fields.Char(
        string='Folio',
    )
    siniestro = fields.Char(
        string='Siniestro',
    )
    siniestro_estatus_id = fields.Many2one(
        comodel_name='fleet.siniestro.estatus',
        string='Estatus del siniestro',
        tracking=True,
    )
    fecha_ingreso_valuacion = fields.Date(
        string='Fecha ingreso a valuación',
        tracking=True,
    )
    fecha_ingreso_reparacion = fields.Date(
        string='Fecha ingreso a reparación',
        tracking=True,
    )
    fecha_compromiso_entrega = fields.Date(
        string='Fecha de comprimiso de entrega',
        tracking=True,
    )
    fecha_entrega = fields.Date(
        string='Fecha de entrega',
        tracking=True,
    )
    fecha_cierre = fields.Date(
        string='Fecha de cierre',
        tracking=True,
    )
    "Informacion del vehiculo"
    vehiculo_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehiculo",
        tracking=True,
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
    "Conductor"
    cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        tracking=True,
    )
    cliente_email = fields.Char(
        string='Email cliente',
    )
    cliente_telefono = fields.Char(
        string='Télefono cliente',
    )
    "Evento"
    fecha_hora_suceso = fields.Date(
        string='Fecha y hora del suceso',
        tracking=True,
    )
    fecha_hora_notifiacion = fields.Date(
        string='Fecha y hora de notificación',
        tracking=True,
    )
    ubicacion = fields.Char(
        string='Ubicación',
        tracking=True,
    )
    conductor = fields.Char(
        string='Conductor',
        tracking=True,
    )
    telefono_conductor = fields.Char(
        string='Telefono conductor',
    )
    descripcion_siniestro = fields.Text(
        string='Descripción del siniestro',
    )
    rec_name = fields.Char(
        string='Nombre',
        compute='_compute_rec_name',
    )

    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for record in self:
            vehiculo = self.env['fleet.vehicle'].browse(record.vehiculo_id.id)
            record.vin_sn = vehiculo.vin_sn
            record.numero_economico = vehiculo.numero_economico
            record.producto_id = vehiculo.producto_id.id
            record.plaza_id = vehiculo.plaza_id.id
            record.cliente_id = vehiculo.driver_id.id
            record.cliente_email = vehiculo.driver_id.email
            record.cliente_telefono = vehiculo.driver_id.phone
            record.conductor = vehiculo.driver_id.name
            record.telefono_conductor = vehiculo.driver_id.phone

    @api.depends('vehiculo_id')
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.id}-{record.folio}-{record.siniestro_tipo_id.name}"
