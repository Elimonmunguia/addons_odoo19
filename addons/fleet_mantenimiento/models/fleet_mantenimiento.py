from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class FleetMantenimiento(models.Model):
    _name = "fleet.mantenimiento"
    _description = "Mantenimiento de vehiculos"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "rec_name"

    etapa_id = fields.Many2one(
        comodel_name="fleet.mantenimiento.etapa",
        string="Etapa",
    )
    proveedor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        domain=[("supplier_rank", ">", 0)],
    )
    fecha_programado = fields.Datetime(
        string="Fecha programado",
        tracking=True,
    )
    folio = fields.Char(
        string="Folio",
    )
    tipo_mantenimiento_id = fields.Many2one(
        comodel_name="fleet.mantenimiento.tipo",
        string="Tipo de mantenimiento",
        tracking=True,
    )
    tipo_mantenimiento_servicio_id = fields.Many2one(
        comodel_name="fleet.mantenimiento.servicio.tipo",
        string = "Km de mantenimiento",
    )
    mostrar_tipo_mant_serv = fields.Boolean(
        string="Mostrar tipo de mantenimiento",
        compute="_compute_mostrar_tipo_mant_serv",
        store=True,
    )
    servicios_ids = fields.Many2many(
        related="tipo_mantenimiento_servicio_id.serivicio_ids",
        string="Servicios incluidos",
    )
    mostrar_servicios = fields.Boolean(
        string="Mostrar servicios",
        compute="_compute_mostrar_servicios",
        store=True,
    )
    km_deteccion = fields.Float(
        string="Km de detección",
        tracking=True,
    )
    km_entrada = fields.Float(
        string="Km de entrada",
        tracking=True,
    )
    fecha_hora_entrada = fields.Datetime(
        string="Fecha y hora de entrada",
        tracking=True,
    )
    fecha_hora_salida = fields.Datetime(
        string="Fecha y hora de salida",
        tracking=True,
    )
    observacion = fields.Text(
        string="Observaciones",
    )
    fecha_deteccion = fields.Date(
        string="Fecha de detección",
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
    conductor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Conductor',
    )
    conductor_email = fields.Char(
        string='Email conductor',
    )
    conductor_telefono = fields.Char(
        string='Telefono conductor',
    )
    "Importes"
    importe = fields.Float(
        string='Importe',
        tracking=True,
    )
    iva = fields.Float(
        string='IVA',
        compute='_compute_iva',
        store=True,
        tracking = True,
    )
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,
        tracking = True,
    )
    "Expediente"
    expediente_digital = fields.Binary(
        string='Expediente',
        attachment=True
    )
    expediente_fotografico = fields.Binary(
        string='Expediente fotografico',
        attachment=True
    )
    "Factura"
    numero_factura = fields.Char(
        string='Numero de factura',
        tracking=True,
    )
    fecha_factura = fields.Date(
        string='Fecha de factura',
        tracking=True,
    )
    "Indicadores"
    indicador_actualizacion = fields.Char(
        string='Indicador de actualizacion',
    )
    rec_name = fields.Char(
        string='Nombre',
        compute='_compute_rec_name',
    )

    @api.model
    def write(self, vals):
        if 'expediente_digital' in vals:
            if vals['expediente_digital']:
                self.message_post(body='📂 Se actualizó o subió un nuevo archivo al expediente digital.')
            else:
                self.message_post(body='🗑️ Se elimino el archivo del expediente digital.')
        if 'expediente_fotografico' in vals:
            if vals['expediente_fotografico']:
                self.message_post(body='📂 Se actualizó o subió un nuevo archivo al expediente fotográfico.')
            else:
                self.message_post(body='🗑️ Se elimino el archivo del expediente fotográfico.')
        if 'etapa_id' in vals:
            if vals['etapa_id'] == 5:
                vehiculo = self.env['fleet.vehicle'].browse(self.vehiculo_id.id)
                vehiculo.write({
                    'km_ult_mantenimiento': self.km_entrada,
                })
                self.env['fleet.vehicle.odometer'].create({
                    'vehicle_id': self.vehiculo_id.id,
                    'value': self.km_entrada,
                    'date': fields.Date.today(),
                })
        res = super(FleetMantenimiento, self).write(vals)
        return res

    @api.depends('tipo_mantenimiento_id')
    def _compute_mostrar_tipo_mant_serv(self):
        for record in self:
            cont = self.env['fleet.mantenimiento.servicio.tipo'].search_count([('mantenimiento_tipo_id', '=', record.tipo_mantenimiento_id.id)])
            if cont > 0:
                record.mostrar_tipo_mant_serv = False
                if not record.tipo_mantenimiento_servicio_id.mantenimiento_tipo_id == record.tipo_mantenimiento_id:
                    record.tipo_mantenimiento_servicio_id = False
                    record.servicios_ids = False
            else:
                record.mostrar_tipo_mant_serv = True
                record.tipo_mantenimiento_servicio_id = False
                record.servicios_ids = False


    @api.depends('tipo_mantenimiento_servicio_id')
    def _compute_mostrar_servicios(self):
        for record in self:
            servicios = self.env['fleet.mantenimiento.servicio.tipo'].browse(record.tipo_mantenimiento_servicio_id.id).serivicio_ids
            if len(servicios) > 0:
                record.mostrar_servicios = False
            else:
                record.mostrar_servicios = True
                record.servicios_ids = False

    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for record in self:
            vehiculo = self.env['fleet.vehicle'].browse(record.vehiculo_id.id)
            record.vin_sn = vehiculo.vin_sn
            record.numero_economico = vehiculo.numero_economico
            record.producto_id = vehiculo.producto_id.id
            record.plaza_id = vehiculo.plaza_id.id
            record.conductor_id = vehiculo.driver_id.id
            record.conductor_email = vehiculo.driver_id.email
            record.conductor_telefono = vehiculo.driver_id.phone

    @api.depends('importe')
    def _compute_iva(self):
        for record in self:
            record.iva = record.importe * 0.16

    @api.depends('importe', 'iva')
    def _compute_total(self):
        for record in self:
            record.total = record.importe + record.iva

    @api.depends('tipo_mantenimiento_id','tipo_mantenimiento_servicio_id')
    def _compute_rec_name(self):
        for record in self:
            if record.tipo_mantenimiento_servicio_id:
                record.rec_name = f"{record.id}-{record.vin_sn}-{record.tipo_mantenimiento_id.name}-{record.tipo_mantenimiento_servicio_id.name}"
            else:
                record.rec_name = f"{record.id}-{record.vin_sn}-{record.tipo_mantenimiento_id.name}"


