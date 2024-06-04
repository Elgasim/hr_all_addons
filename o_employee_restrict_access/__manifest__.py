# -*- coding: utf-8 -*-
{
    'name': "Appness HR :Restrict Employee Access",
    'summary': """Restrict access to certain employee profiles to a designated group (for example Top Management profiles)""",
    'description': """Restrict access to certain employee profiles to a designated group (for example Top Management profiles)""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['hr'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/access.xml',
        'views/views.xml',
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