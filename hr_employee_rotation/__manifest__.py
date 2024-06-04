# -*- coding: utf-8 -*-
{
    'name': "Appness HR :Employee Rotation",
    'summary': """Ability to rotation employee to another job in same department .""",
    'description': """Ability to rotation employee to another job in same department .""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['hr','hr_contract','nus_base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_rotation.xml',
        'data/schedule_rotation.xml',
        'views/access_rule.xml',
        'data/mail_activity_data.xml',
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