# -*- coding: utf-8 -*-
{
    'name': "Appness HR : Employee Directory",
    'summary': """This Module contain employee main profile """,
    'description': """This Module contain employee main profile""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee.xml",
        "views/res_config_setting.xml",
        "data/employee_notification.xml",
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