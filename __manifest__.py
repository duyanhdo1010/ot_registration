{
    'name': 'OT Registration',
    'version': '12.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Quan ly dang ky OT',
    'depends': ['base', 'mail', 'hr', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/ot_sequence.xml',
        'views/ot_category_views.xml',
        'views/ot_request_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}