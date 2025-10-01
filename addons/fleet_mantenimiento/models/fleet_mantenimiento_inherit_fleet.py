from odoo import fields,models,api

import logging
_logger = logging.getLogger(__name__)

class FleetMantenimientoInheritFleet(models.Model):
    _inherit = 'fleet.vehicle'

    "Semaforo de mantenimiento"
    km_ult_mantenimiento = fields.Float(
        string='Km último mantenimiento',
    )
    km_prox_mantenimiento = fields.Float(
        string='Km próximo mantenimiento',
    )
    diferencia_prox_mantenimiento = fields.Float(
        string='Diferencia próximo mantenimiento',
        compute='_compute_diferencia_prox_mantenimiento',
        store=True,
    )
    color_semaforo = fields.Integer(
        string='Color semáforo',
        compute='_compute_color_semaforo',
        store=True,
    )
    mantenimiento_proximo_id = fields.Many2one(
        comodel_name='fleet.mantenimiento.servicio.tipo',
        string='Mantenimiento próximo',
    )

    @api.depends('km_prox_mantenimiento','odometro_mod')
    def _compute_diferencia_prox_mantenimiento(self):
        for record in self:
            record.diferencia_prox_mantenimiento = record.km_prox_mantenimiento - record.odometro_mod

    @api.depends('diferencia_prox_mantenimiento')
    def _compute_color_semaforo(self):
        for vehiculo in self:
            if vehiculo.diferencia_prox_mantenimiento >= 1000:
                vehiculo.color_semaforo = 10
            elif vehiculo.diferencia_prox_mantenimiento < 1000 and vehiculo.diferencia_prox_mantenimiento >= 500:
                vehiculo.color_semaforo = 3
                vehiculo.crear_mantenimiento_action()
            elif vehiculo.diferencia_prox_mantenimiento < 500 and vehiculo.diferencia_prox_mantenimiento >= 0:
                vehiculo.color_semaforo = 2
                vehiculo.crear_mantenimiento_action()
            elif vehiculo.diferencia_prox_mantenimiento < 0:
                vehiculo.color_semaforo = 1
                vehiculo.crear_mantenimiento_action()

    def crear_mantenimiento2(self):
        tipo_mantenimientos = self.env['fleet.mantenimiento.servicio.tipo'].search([('mantenimiento_tipo_id','=', 1)])
        mantenimientos = tipo_mantenimientos.sorted(key=lambda x: x.valor)
        primer_mantenimiento = mantenimientos.filtered(lambda x: x.es_primer_mantenimiento == True)
        for vehiculo in self:
            if vehiculo.km_ult_mantenimiento < primer_mantenimiento.valor:
                vehiculo.km_prox_mantenimiento = primer_mantenimiento.valor
                vehiculo.mantenimiento_proximo_id = primer_mantenimiento.id
            else:
                mantenimiento_hechos = self.env['fleet.mantenimiento'].search([('etapa_id', '=', 5), ('tipo_mantenimiento_id', '=', 1)])
                mantenimientos_vehiculo = mantenimiento_hechos.filtered(lambda m: m.vehiculo_id.id == vehiculo.id)
                if mantenimientos_vehiculo:
                    ultimo = max(mantenimientos_vehiculo, key=lambda x: x.create_date)
                else:
                    ultimo = False
                valor_mantenimiento_anterior = 0
                for i, mantenimiento in enumerate(mantenimientos):
                    if (vehiculo.km_ult_mantenimiento <= mantenimiento.valor and vehiculo.km_ult_mantenimiento >= valor_mantenimiento_anterior and ultimo and ultimo.etapa_id and ultimo.etapa_id.id in [5, 6]):
                        valor_mantenimiento_anterior = mantenimientos[i].valor
                        vehiculo.mantenimiento_proximo_id = mantenimientos[i]
                        vehiculo.km_prox_mantenimiento = vehiculo.km_ult_mantenimiento + 10000

    def crear_mantenimiento_action(self):
        mantenimientos = self.env['fleet.mantenimiento'].search([('tipo_mantenimiento_id', '=', 1),('vehiculo_id', '=', self.id)])
        if mantenimientos:
            for mantenimiento in mantenimientos:
                if mantenimiento.tipo_mantenimiento_id == self.mantenimiento_proximo_id.mantenimiento_tipo_id.id and mantenimiento.tipo_mantenimiento_servicio_id == self.mantenimiento_proximo_id.id:
                    if self:
                        self.crear_mantenimiento()
                else:
                    print("Mantenimiento ya realizado")
        else:
            self.crear_mantenimiento()


    def crear_mantenimiento(self):
        self.env['fleet.mantenimiento'].create({
            'etapa_id': 1,
            'tipo_mantenimiento_id': self.mantenimiento_proximo_id.mantenimiento_tipo_id.id,
            'tipo_mantenimiento_servicio_id': self.mantenimiento_proximo_id.id,
            'vehiculo_id': self.id,
            'fecha_deteccion': fields.Date.today(),
            'km_deteccion': self.odometer,
        })