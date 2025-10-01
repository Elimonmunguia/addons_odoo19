from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class fleet_adecuacion(models.Model):
    _name = 'fleet.adecuacion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rec_name'
    _description = 'Adecuaciones de vehiculos'

    "Informacion general"
    adecuacion_id  = fields.Many2one(
        comodel_name='fleet.adecuacion.catalogo',
        string='Tipo de adecuación',
        tracking=True
    )
    fecha_instalacion = fields.Date(
        string='Fecha de instalación',
        tracking=True
    )
    num_serie = fields.Char(
        string='N° de serie',
        tracking=True
    )
    imei = fields.Char(
        string='IMEI',
        tracking=True
    )
    marca = fields.Char(
        string='Marca',
    )
    modelo = fields.Char(
        string='Modelo',
    )
    proveedor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Proveedor',
        domain=[('supplier_rank', '>', 0)]
    )
    "Importe"
    instalacion_incluida = fields.Boolean(
        string='Instalación incluida',
        tracking=True
    )
    incluido_valor_vehiculo = fields.Boolean(
        string='Incluido en valor del vehículo',
        tracking=True
    )
    importe = fields.Float(
        string='Importe',
        tracking=True
    )
    iva = fields.Float(
        string='IVA',
        compute='_compute_iva',
        tracking=True,
        store=True
    )
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        tracking=True,
        store=True
    )
    total_general = fields.Float(
        string='Total general',
        compute='_compute_total_general',
        tracking=True,
        store=True
    )
    "Infromación del vehiculo"
    vehiculo_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehículo',
        tracking=True
    )
    numero_economico = fields.Char(
        string='N° de economico',
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
    rec_name = fields.Char(
        string='Recibo',
        compute='_compute_rec_name',
    )

    "Instalación"
    instalacion_proveedor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Proveedor',
        domain=[('supplier_rank', '>', 0)]
    )
    instalacion_importe = fields.Float(
        string='Importe',
    )
    instalacion_iva = fields.Float(
        string='IVA',
        compute='_compute_instalacion_iva',
        store=True
    )
    instalacion_total = fields.Float(
        string='Total',
        compute='_compute_instalacion_total',
        store=True
    )
    "Documentos"
    expediente_arch = fields.Binary(
        string='Expediente',
        attachment=True,
    )

    @api.depends('importe')
    def _compute_iva(self):
        for record in self:
            record.iva = record.importe * 0.16

    @api.depends('importe', 'iva')
    def _compute_total(self):
        for record in self:
            record.total = record.importe + record.iva

    @api.depends('instalacion_importe')
    def _compute_instalacion_iva(self):
        for record in self:
            record.instalacion_iva = record.instalacion_importe * 0.16

    @api.depends('instalacion_importe','instalacion_iva')
    def _compute_instalacion_total(self):
        for record in self:
            record.instalacion_total = record.instalacion_importe + record.instalacion_iva

    @api.depends('instalacion_total','total')
    def _compute_total_general(self):
        for record in self:
            record.total_general = record.total + record.instalacion_total

    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for record in self:
            vehiculo = self.env['fleet.vehicle'].browse(record.vehiculo_id.id)
            record.vin_sn = vehiculo.vin_sn
            record.numero_economico = vehiculo.numero_economico
            record.producto_id = vehiculo.producto_id.id
            record.plaza_id = vehiculo.plaza_id.id

    @api.model
    def create(self, vals):
        res = super(fleet_adecuacion, self).create(vals)
        if 'expediente_arch' in vals and vals['expediente_arch']:
                res.message_post(body='✔️ Se subió un nuevo archivo al expediente.')
        return res

    @api.model
    def write(self, vals):
        if 'expediente_arch' in vals:
            if vals['expediente_arch']:
                self.message_post(body='📂 Se actualizó o subió un nuevo archivo al expediente.')
            else:
                self.message_post(body='🗑️ Se elimino el archivo del expediente.')
        instalacion = vals.get('instalacion_incluida')
        if instalacion:
            vals['instalacion_importe'] = 0
            vals['instalacion_iva'] = 0
            vals['instalacion_total'] = 0
        res = super(fleet_adecuacion, self).write(vals)
        return res

    @api.model
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.id}-{record.vin_sn}-{record.adecuacion_id.name}"