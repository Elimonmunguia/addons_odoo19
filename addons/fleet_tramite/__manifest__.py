{
    'name': 'Fleet Customer - Tramites',
    'version': '1.0',
    'author': 'Jorge Eduardo Limon Munguia <jorge.limon@fuentebuena.com>',
    'description': 'Módulo personalizado para registrar los tramites de los vehículos',
    'depends': [
        'fleet_customer',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_tramite_motivo_pago_view.xml',
        'views/fleet_tramite_tipo_view.xml',
        'views/fleet_tramite_view.xml',
        'views/fleet_tramite_fleet_view.xml',
        'views/fleet_tramite_menu.xml'
    ],
    'application': True,
    'installable': True
}