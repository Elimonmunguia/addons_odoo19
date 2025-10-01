from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class FleetContrato(models.Model):
    _inherit = 'fleet.vehicle.log.contract'
    _description = 'Módulo personalizado para registrar los contratos para los vehículos'
    _rec_name = 'rec_name'

    cie = fields.Char(
        string='CIE',
        tracking=True
    )
    cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        compute='_compute_datos_vehiculo',
        store=True,
        tracking=True
    )
    nombre_cliente = fields.Char(
        string='Nombre del cliente',
    )
    num_plazos = fields.Integer(
        string='N° de plazos'
    )
    condicion_vehiculo_id = fields.Many2one(
        comodel_name='fleet.contrato.condicion.vehiculo',
        string='Condición del vehículo',
    )
    id_solicitud = fields.Char(
        string='ID de solicitud'
    )
    "Cancelación"
    fecha_cancelacion = fields.Date(
        string='Fecha de cancelación',
        tracking=True
    )
    motivo_cancelacion_id = fields.Many2one(
        comodel_name='fleet.contrato.motivo.cancelacion',
        string='Motivo de cancelación'
    )
    cancelado = fields.Boolean(
        string='Cancelado'
    )
    rec_name = fields.Char(
        string='rec_name',
        compute='_compute_rec_name',
    )
    "Importes"
    importe_garantia = fields.Float(
        string='Importe de garantia',
        tracking=True
    )
    "Información del vehiculo"
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
    "Documentos"
    attach_contrato = fields.Binary(
        string='Contrato',
    )

    @api.model
    def create(self, vals):
        contrato = self.search_count([('vehicle_id', '=', vals['vehicle_id'])])
        if contrato == 0:
            vals['condicion_vehiculo_id'] = 1
        else:
            vals['condicion_vehiculo_id'] = 2
        res = super(FleetContrato, self).create(vals)
        if 'attach_contrato' in vals and vals['attach_contrato']:
            res.message_post(body='✔️ Se subió un nuevo archivo al expediente.')
        return res

    def cancelar_contrato(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancelación de contrato',
            'res_model': 'fleet.contrato.cancelacion',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('fleet_contrato.fleet_contrato_cancelacion_view_form').id
        }

    @api.depends('vehicle_id')
    def _compute_datos_vehiculo(self):
        for record in self:
            vehiculo = self.env['fleet.vehicle'].browse(record.vehicle_id.id)
            record.vin_sn = vehiculo.vin_sn
            record.numero_economico = vehiculo.numero_economico
            record.producto_id = vehiculo.producto_id.id
            record.plaza_id = vehiculo.plaza_id.id
            record.cliente_id = vehiculo.driver_id.id

    @api.model
    def write(self, vals):
        if 'attach_contrato' in vals:
            if vals['attach_contrato']:
                self.message_post(body='📂 Se actualizó o subió un nuevo archivo al expediente.')
            else:
                self.message_post(body='🗑️ Se elimino el archivo del expediente.')
        res = super(FleetContrato, self).write(vals)
        return res

    @api.model
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.id}-{record.vin_sn}-{record.ins_ref}"