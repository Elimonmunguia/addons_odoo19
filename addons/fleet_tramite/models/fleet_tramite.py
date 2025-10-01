from odoo import models, fields, api


class FleetTramite(models.Model):
    _name = 'fleet.tramite'
    _rec_name = 'rec_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Fleet Tramite'

    "Información"
    tipo_tramite_id = fields.Many2one(
        comodel_name='fleet.tramite.tipo',
        string='Tipo de tramite',
        tracking=True
    )
    folio = fields.Char(
        string='Folio',
        tracking=True
    )
    fecha_tramite = fields.Date(
        string='Fecha tramite',
        tracking=True
    )
    fecha_vencimiento_renovacion = fields.Date(
        string='Fecha vencimiento renovacion',
        tracking=True
    )
    dependencia = fields.Char(
        string='Dependencia',
    )
    estado = fields.Many2one(
        comodel_name='res.country.state',
        string='Estado',
        domain=[('country_id', '=', 'MX')],
    )
    motivo_pago_id = fields.Many2one(
        comodel_name='fleet.tramite.motivo.pago',
        string='Motivo de pago',
    )
    rec_name = fields.Char(
        string='Rec Name',
        compute='_compute_rec_name',
    )
    "Pago"
    importe = fields.Float(
        string='Importe',
        tracking=True
    )
    aplica_iva = fields.Boolean(
        string='¿Aplica IVA?',
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
    "Información del vehiculo"
    vehiculo_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehiculo',
        tracking=True
    )
    vin_sn = fields.Char(
        string='VIN',
        compute='_compute_datos_vehiculo',
        store=True
    )
    numero_economico = fields.Char(
        string='N° Economico',
        compute='_compute_datos_vehiculo',
        store=True,
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
    "Observaciones"
    observacion = fields.Text(
        string='Observaciones',
    )
    "Adjuntos"
    expediente = fields.Binary(
        string='Expediente',
    )


    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for record in self:
            if record.vehiculo_id:
                vehiculo = self.env['fleet.vehicle'].browse(record.vehiculo_id.id)
                record.vin_sn = vehiculo.vin_sn
                record.numero_economico = vehiculo.numero_economico
                record.producto_id = vehiculo.producto_id.id
                record.plaza_id = vehiculo.plaza_id.id

    @api.model
    def create(self, vals):
        res = super(FleetTramite, self).create(vals)
        if 'expediente' in vals and vals['expediente']:
            res.message_post(body='✔️ Se subió un nuevo archivo al expediente.')
        return res

    @api.model
    def write(self, vals):
        if 'expediente' in vals:
            if vals['expediente']:
                self.message_post(body='📂 Se actualizó o subió un nuevo archivo al expediente.')
            else:
                self.message_post(body='🗑️ Se elimino el archivo del expediente.')
        res = super(FleetTramite, self).write(vals)
        return res

    @api.depends('aplica_iva', 'importe')
    def _compute_iva(self):
        for record in self:
            if record.aplica_iva:
                record.iva = record.importe * 0.16
            else:
                record.iva = 0.0

    @api.depends('importe', 'iva')
    def _compute_total(self):
        for record in self:
            if record.aplica_iva:
                record.total = record.importe + record.iva
            else:
                record.total = record.importe

    @api.model
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.id}-{record.vin_sn}-{record.tipo_tramite_id.name}"