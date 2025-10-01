from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class FleetCustomerInheritFleet(models.Model):
    _inherit = 'fleet.vehicle'
    _rec_name = 'rec_name'

    ultimo_cambio_etapa = fields.Date(
        string='Último cambio de etapa',
    )
    numero_economico = fields.Char(
        string='Número economico',
    )
    proveedor_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('supplier_rank', '>', 0)],
        string='Proveedor',
    )
    es_gnv = fields.Boolean(
        string='GNV'
    )
    fecha_puesta_punto = fields.Datetime(
        string='Fecha puesta punto',
    )
    condicion_vehiculo_id = fields.Many2one(
        comodel_name='fleet.customer.condicion.vehiculo',
        string='Condición del vehículo',
    )
    uso_vehiculo_id = fields.Many2one(
        comodel_name='fleet.customer.uso.vehiculo',
        string='Uso de vehículo',
    )
    flotilla_id = fields.Many2one(
        comodel_name='fleet.customer.flotilla',
        string='Flotilla',
    )
    sub_etapa_id = fields.Many2one(
        comodel_name='fleet.customer.sub.etapa',
        string='Sub etapa',
        domain="[('id', 'in', sub_etapas_ids)]",
    )
    sub_etapas_ids = fields.Many2many(
        comodel_name='fleet.customer.sub.etapa',
        related='state_id.sub_etapa_ids',
        string='Sub etapas',
    )
    mostrar_sub_etapa = fields.Boolean(
        string='Mostrar sub etapa',
        compute='_compute_mostar_sub_etapa',
    )
    producto_id = fields.Many2one(
        comodel_name='fleet.customer.producto',
        string='Producto',
    )
    plaza_id = fields.Many2one(
        comodel_name='fleet.customer.plaza',
        string='Plaza',
    )
    baja = fields.Boolean(
        string='¿Es baja?',
    )
    motivo_baja_id = fields.Many2one(
        comodel_name='fleet.customer.motivo.baja',
        string='Motivo de baja'
    )
    fecha_baja  = fields.Date(
        string='Fecha de baja',
    )
    color_interior = fields.Char(
        string='Color interior',
    )
    "Adquisición"
    fecha_adquisicion = fields.Date(
        string='Fecha adquisición',
    )
    condicion_adquisicion_id = fields.Many2one(
        comodel_name='fleet.customer.condicion.vehiculo',
        string='Condición adquisición',
    )
    "Factura"
    factura = fields.Char(
        string='Factura',
    )
    fecha_factura = fields.Date(
        string='Fecha factura',
    )
    folio_uuid = fields.Char(
        string='Folio UUID',
    )
    fecha_carta_porte = fields.Date(
        string='Fecha carta porte',
    )
    folio_carta_porte = fields.Char(
        string='Folio carta porte',
    )
    "Orden de compra"
    fecha_recepcion = fields.Date(
        string='Fecha recepción',
    )
    orden_compra = fields.Char(
        string='Orden de compra',
    )
    fecha_orden_compra = fields.Date(
        string='Fecha orden de compra',
    )
    "Importes de adquisición"
    importe_adquisicion = fields.Float(
        string='Importe adquisición',
    )
    iva_adquisicion = fields.Float(
        string='IVA adquisición',
    )
    importe_total_adquisicion = fields.Float(
        string='Importe total adquisición',
    )
    valor_residual_adquisicion = fields.Float(
        string='Valor residual adquisición',
    )
    "Documentos"
    factura_vehiculo = fields.Binary(
        string='Factura vehículo',
        attachment=True
    )
    opcion_compra = fields.Binary(
        string='Opcion compra',
        attachment=True
    )
    "Adicionales"
    odometro_mod = fields.Float(
        string='Odómetro mod',
    )
    rec_name = fields.Char(
        string='Rec name',
        compute='_compute_rec_name',
    )
    "Reacondicionamiento"
    fecha_prox_reacondicionamiento = fields.Date(
        string='Fecha reacondicionamiento',
    )
    mostrar_fecha_prox_reacond = fields.Boolean(
        string='Mostrar fecha de reacondicionamiento',
        compute='_compute_mostrar_fecha_prox_reacond',
    )
    mostrar_driver = fields.Boolean(
        string='Mostrar driver',
        compute='_compute_mostrar_driver',
    )
    version = fields.Many2one(
        comodel_name='fleet.customer.version',
        string='Versión',
    )
    numero_motor = fields.Char(
        string='Número de motor',
    )
    nombre_modelo = fields.Char(
        string='Nombre del modelo',
        related='model_id.name',
    )

    @api.depends('state_id')
    def _compute_mostrar_driver(self):
        for vehiculo in self:
            if vehiculo.state_id.es_estapa_alta or vehiculo.state_id.es_etapa_recibido:
                vehiculo.mostrar_driver = False
            else:
                vehiculo.mostrar_driver = True

    @api.depends('state_id')
    def _compute_mostrar_fecha_prox_reacond(self):
        for vehiculo in self:
            if vehiculo.state_id.es_etapa_reacondicionamiento:
                vehiculo.mostrar_fecha_prox_reacond = True
            else:
                vehiculo.mostrar_fecha_prox_reacond = False

    @api.depends('state_id')
    def _compute_mostar_sub_etapa(self):
        for vehiculo in self:
            if len(vehiculo.sub_etapas_ids) > 1:
                vehiculo.mostrar_sub_etapa = True
            else:
                vehiculo.mostrar_sub_etapa = False

    @api.depends('model_id','vin_sn')
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.model_id.name}/{record.vin_sn}"

    @api.model
    def create(self, vals):
        uso_id = self.env['fleet.customer.uso.vehiculo'].browse(1)
        for val in vals:
            if uso_id:
                val['uso_vehiculo_id'] = uso_id.id
        res = super(FleetCustomerInheritFleet, self).create(vals)
        res.calcular_num_economico()
        return res

    # @api.model
    # def write(self, vals):
    #     if 'state_id' in vals:
    #         state = self.env['fleet.vehicle.state'].search([('id', '=', vals['state_id'])])
    #         for vehiculo in self:
    #             vehiculo.fecha_prox_reacondicionamiento = False
    #             vehiculo.sub_etapa_id = False
    #             if not vehiculo.fecha_recepcion and not state.es_estapa_alta:
    #                 raise ValidationError('No se puede cambiar de etapa sin fecha de recepción')
    #         vals['ultimo_cambio_etapa'] = fields.Date.today()
    #     res = super(FleetCustomerInheritFleet, self).write(vals)
    #     return res

    @api.constrains('vin_sn')
    def _check_vin_sn(self):
        vin = self.vin_sn
        num_coches =self.search_count([('vin_sn', '=', vin)])
        if num_coches > 1:
            raise ValidationError('No se puede utilizar el mismo VIN para dos o mas vehículos')

    def dar_baja(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Baja de vehiculo',
            'res_model': 'fleet.customer.baja',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('fleet_customer.fleet_customer_baja_view_form').id
        }

    def calcular_num_economico(self):
        prefijo_modelo = self.model_id.prefijo or ''
        year_modelo = str(self.model_year)[-1]
        prefijo_producto =  self.producto_id.prefijo
        if prefijo_producto == 'P':
            prefijo_producto = ''
        prefijo = prefijo_producto + prefijo_modelo
        registros_similares = self.search([('numero_economico','like', prefijo + '%')])
        nuevo_consecutivo = 1
        consecutivos_excistentes = []
        for registro in registros_similares:
            if registro.numero_economico and len(registro.numero_economico) >= len(prefijo) + 4:
                try:
                    consecutivo = int(registro.numero_economico[-4:])
                    consecutivos_excistentes.append(consecutivo)
                except ValueError:
                    pass
        if consecutivos_excistentes:
            nuevo_consecutivo = max(consecutivos_excistentes) + 1
        consecutivo_str = ('%04d' % nuevo_consecutivo)
        nuevo_id = prefijo + year_modelo + consecutivo_str
        self.write({
            'numero_economico': nuevo_id
        })