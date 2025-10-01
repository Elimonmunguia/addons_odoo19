from odoo import  fields, models


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    numero_empleado = fields.Char(
        string='Número de empleado'
    )
    fecha_ingreso = fields.Date(
        string='Fecha de ingreso'
    )