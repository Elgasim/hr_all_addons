# -*- coding: utf-8 -*-
{
    'name': "Appness HR : Salary Grade 2",
    'summary': """Salary Wage By Grade """,
    'description': """Salary Wage By Grade""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['hr_contract_grade_base'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
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