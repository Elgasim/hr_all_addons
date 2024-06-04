# -*- coding: utf-8 -*-
{
    'name': "Appness HR : Contract Benefits",
    'summary': """Contract Benefits""",
    'description': """Contract Beneftis""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['hr_employee_main','hr_contract'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/grade_benefit.xml',
        'views/hr_contract.xml',
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