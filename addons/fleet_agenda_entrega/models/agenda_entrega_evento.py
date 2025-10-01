from odoo import fields, models, api


class AgendaEntregaEvento(models.Model):
    _name = "agenda.entrega.evento"
    _description = "Agenda Entrega Evento"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    agenda_id = fields.Many2one(
        comodel_name="agenda.entrega",
        string="Agenda"
    )
    tipo_evento_id = fields.Many2one(
        comodel_name="agenda.entrega.tipo.evento",
    )
    descripcion = fields.Text(
        string="Descripción",
        tracking=True
    )
    status_id = fields.Many2one(
        comodel_name="agenda.entrega.estatus.evento",
        string="Estatus de evento",
        tracking=True
    )
    mostrar_status = fields.Boolean(
        string="Mostrar status",
        compute="_compute_mostrar_status",
    )
    estatus_id = fields.Many2one(
        comodel_name="agenda.entrega.estatus.evento",
        string="Estatus de evento",
        domain="[('id', '=', 4)]",
    )
    mostrar_estatus = fields.Boolean(
        string="Mostrar estatus",
        compute="_compute_mostrar_status",
    )
    descripcion_solventacion = fields.Text(
        string="Descripción de Solventación",
        tracking=True
    )

    @api.depends("status_id")
    def _compute_mostrar_status(self):
        for evento in self:
            if evento.status_id.id in [1,2,3]:
                evento.mostrar_status = False
            else:
                evento.mostrar_status = True
            if evento.status_id.id == 4:
                evento.mostrar_estatus = False
            else:
                evento.mostrar_estatus = True

    def action_solventar(self):
        self.status_id = 3

    def action_enviar_revision(self):
        return  {
            'type': 'ir.actions.act_window',
            'name': 'Solventar',
            'res_model': 'evento.solventar.wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('fleet_agenda_entrega.solventar_view_form').id
        }

    def action_reincidencia(self):
        self.status_id = 4
        self.estatus_id = 4