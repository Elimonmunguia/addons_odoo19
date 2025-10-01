from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)

class Evento(models.TransientModel):
    _name = 'agenda.entrega.evento.wizard'
    _description = 'Agenda Entrega Evento Wizard'

    agenda_id = fields.Many2one(
        comodel_name="agenda.entrega",
        string="Agenda"
    )
    tipo_evento_id = fields.Many2one(
        comodel_name="agenda.entrega.tipo.evento",
    )
    descripcion = fields.Text(
        string="Descripción"
    )
    status_id = fields.Many2one(
        comodel_name="agenda.entrega.estatus.evento",
        string="Estatus de evento"
    )
    descripcion_solventacion = fields.Text(
        string="Descripción de Solventación"
    )

    def action_confirm(self):
        self.env['agenda.entrega.evento'].sudo().create({
            'agenda_id':  self.env.context.get('active_id'),
            'tipo_evento_id': self.tipo_evento_id.id,
            'descripcion': self.descripcion,
            'status_id': 1
        })
        self.env['bus.bus']._sendone(
            self.env.user.partner_id,
            'simple_notification',
            {
                'type': 'success',
                'message': 'Evento creado correctamente',
                'sticky': False,
            }
        )
        return { 'type': 'ir.actions.act_window_close'}