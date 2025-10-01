{
    'name': 'Fleet Siniestro',
    'version': '1.0',
    'author': 'Jorge Eduardo Limon Munguia <jorge.limon@fuentebuena.com>',
    'description': 'Módulo de siniestro de pilotea',
    'depends': [
        'fleet_customer',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_siniestro_estatus_view.xml',
        'views/fleet_siniestro_movilidad_view.xml',
        'views/fleet_siniestro_tipo_view.xml',
        'views/fleet_siniestro_fase_view.xml',
        'views/fleet_siniestro_etapa_view.xml',
        'views/fleet_siniestro_view.xml',
        'views/fleet_siniestro_menu.xml',
    ],
    'application': False,
    'installable': True
}