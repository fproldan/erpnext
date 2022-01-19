from __future__ import unicode_literals

data = {
    'modules': [
        'Assets'
    ],
    'restricted_roles': [
        'Asset Maintenance Manager',
        'Asset Maintenance User'
    ],
    'on_setup': 'erpnext.assets.setup.setup_assets',
    'remove_dashboard': 'erpnext.assets.setup.remove_dashboard'
}