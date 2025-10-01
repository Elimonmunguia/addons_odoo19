from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class AgendaEntrega(models.Model):
    _name = 'agenda.entrega'
    _description = 'Agenda Entrega'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rec_name'


    etapa_id = fields.Many2one(
        comodel_name='agenda.entrega.etapa',
        string='Etapa',
        default=1
    )
    "Dictamen"
    dictamen_id = fields.Many2one(
        comodel_name='agenda.entrega.dictamen',
        string='Dictamen'
    )
    estatus_dictamen = fields.Many2one(
        comodel_name="agenda.entrega.estatus.dictamen",
        string="Estatus de dictamen",
        compute='_compute_datos_dictamen',
        store=True
    )
    email_cliente = fields.Char(
        string="Email"
    )
    telefono_cliente = fields.Char(
        string="Telefono"
    )
    "Solicitud"
    asesor_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Asesor'
    )
    num_empleado = fields.Char(
        string='Num. Empleado'
    )
    fecha_entrega = fields.Date(
        string='Fecha de entrega'
    )
    lugar_entrega_id = fields.Many2one(
        comodel_name='agenda.entrega.lugar',
        string='Lugar de entrega'
    )
    indicaciones = fields.Text(
        string='Indicaciones'
    )
    canalizacion_id = fields.Many2one(
        comodel_name='agenda.entrega.canalizacion',
        string='Canalizacion'
    )
    "Vehiculo"
    vehiculo_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehiculo"
    )
    modelo_vehiculo_id = fields.Many2one(
        comodel_name="fleet.vehicle.model",
        string="Modelo",
        compute = '_compute_datos_vehiculo',
        store=True
    )
    version = fields.Many2one(
        comodel_name='fleet.customer.version',
        string='Version',
        compute='_compute_datos_vehiculo',
        store=True
    )
    vin_sn = fields.Char(
        string='VIN',
        compute='_compute_datos_vehiculo',
        store=True
    )
    condicion_vehiculo_id = fields.Many2one(
        comodel_name='fleet.customer.condicion.vehiculo',
        string='Condicion',
        compute='_compute_datos_vehiculo',
        store=True
    )
    color = fields.Char(
        string='Color',
        compute='_compute_datos_vehiculo',
        store=True
    )
    year = fields.Char(
        string='Year',
        compute = '_compute_datos_vehiculo',
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
    "Mesa de control"
    req_instrumentacion = fields.Many2one(
        comodel_name='agenda.entrega.estatus.instru',
        string='Requerimientos de instrumentacion'
    )
    estatus_comprobante_deposito = fields.Many2one(
        comodel_name='agenda.entrega.estatus.comprobante',
        string='Estatus comprobante depósito'
    )
    "Entrega"
    fecha_confirmada = fields.Date(
        string='Fecha confirmada'
    )
    ejecutivo_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Ejecutivo'
    )
    nota = fields.Text(
        string='Nota'
    )
    autorizacion_uso = fields.Boolean(
        string='Autorizacion de uso de datos'
    )
    foto_entrega = fields.Binary(
        string='Foto de entrega',
        attachment=True
    )
    "Adición"
    contador = fields.Integer(
        string='Contador',
        compute='_compute_contador'
    )
    rec_name = fields.Char(
        string='Rec name',
        compute='_compute_rec_name'
    )
    mostrar_evento = fields.Boolean(
        string='Mostrar evento',
        compute='_compute_mostrar_evento',
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        self.env.cr.commit()
        template = self.env.ref('fleet_agenda_entrega.agenda_entrega_mail_template')
        template.send_mail(
            res.id,
            force_send=True,
            email_values= {
                'email_to': 'jorge.limon@fuentebuena.com.mx'
            }
        )
        return res

    @api.depends('vin_sn','lugar_entrega_id')
    def _compute_rec_name(self):
        for record in self:
            record.rec_name = f"{record.id}-{record.vin_sn}-{record.lugar_entrega_id.name}"

    def _compute_contador(self):
        for record in self:
            num_eventos = self.env['agenda.entrega.evento'].search_count([('agenda_id', '=', record.id),('status_id', '=', 1)])
            record.contador = num_eventos

    def crear_evento(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'agenda.entrega.evento.wizard',
            'name': 'Evento',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('fleet_agenda_entrega.evento_view_form').id
        }

    def mostrar_eventos(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'agenda.entrega.evento',
            'name': 'Eventos',
            'view_mode': 'list,form',
            'taget': 'new',
            'domain': [('agenda_id', '=', self.id),('status_id', '=', 1)]
        }

    @api.depends('vehiculo_id')
    def _compute_datos_vehiculo(self):
        for vehiculo in self:
            coche = self.env['fleet.vehicle'].browse(vehiculo.vehiculo_id.id)
            vehiculo.modelo_vehiculo_id = coche.model_id.id
            vehiculo.version = coche.version.id
            vehiculo.vin_sn = coche.vin_sn
            vehiculo.condicion_vehiculo_id = coche.condicion_vehiculo_id.id
            vehiculo.color = coche.color
            vehiculo.year = coche.model_year
            vehiculo.producto_id = coche.producto_id.id
            vehiculo.plaza_id = coche.plaza_id.id

    @api.depends('dictamen_id')
    def _compute_datos_dictamen(self):
        for dictamen in self:
            dictamen_consul = self.env['agenda.entrega.dictamen'].browse(dictamen.dictamen_id.id)
            dictamen.estatus_dictamen = dictamen_consul.status_dictamen.id
            dictamen.email_cliente = dictamen_consul.email_cliente
            dictamen.telefono_cliente = dictamen_consul.telefono_cliente

    def _compute_mostrar_evento(self):
        for record in self:
            contador = self.env['agenda.entrega.evento'].search_count([('agenda_id', '=', record.id)])
            if contador > 0:
                record.mostrar_evento = True
            else:
                record.mostrar_evento = False