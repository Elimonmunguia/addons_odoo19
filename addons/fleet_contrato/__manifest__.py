{
    'name': 'Fleet Customer - Contratos',
    'version': '1.0',
    'category': 'Fleet',
    'description': 'Módulo personalizado para registrar los contratos para los vehículos',
    'author': 'Jorge Eduardo Limon Munguia <jorge.limon@fuentebuena.com>',
    'depends': [
        'fleet_customer'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_contrato_condicion_vehiculo_view.xml',
        'views/fleet_contrato_motivo_cancelacion_view.xml',
        'views/fleet_contrato_view.xml',
        'wizard/fleet_contrato_cancelacion.xml',
        'views/fleet_contrato_menu.xml'
    ],
    'application': False,
    'installable': True
}