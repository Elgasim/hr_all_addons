# -*- coding: utf-8 -*-
{
    'name': "Appness HR : Emmployee Rotation Multi Company",
    'summary': """Manager can transfer employee to another company (in case it’s multi company system )""",
    'description': """Manager can transfer employee to another company (in case it’s multi company system )""",
    'category': 'HR',
    'version': '17.0',
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    # any module necessary for this one to work correctly
    'depends': ['hr','hr_employee_main','hr_employee_rotation'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/access_rule.xml',
        'views/employee_transfer.xml',
        'views/schedule_transfer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}