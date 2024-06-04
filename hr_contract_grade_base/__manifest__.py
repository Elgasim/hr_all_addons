# -*- coding: utf-8 -*-
{
    'name': "Appness HR : Salary Grade",
    'summary': """Salary Wage By Grade """,
    'description': """Salary Wage By Grade""",
    'author': "Appness Technology",
    'website': "http://www.appness.net",
    'category': 'HR',
    'version': '17.0',
    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_account_community','hr_contract_benefit'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/configuration.xml',
        'views/contract_inherit.xml',
        'data/contract_notification.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
     #   'demo.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
