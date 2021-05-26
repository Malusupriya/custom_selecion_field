{
    'name': "Custom Selection Field",

    'summary': """ """,

    'description': """
        Adding color to dropdown in selection field-odoo14
    """,

    'author': "Bista Solutions Pvt. Ltd",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'web',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'web'],

    # always loaded
    'data': [
        'view/view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        # 'static/src/xml/base.xml'
    ],
}
# -*- coding: utf-8 -*-
