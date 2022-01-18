from __future__ import unicode_literals

data = {
    'modules': [
        'Projects'
    ],
    'restricted_roles': [
        'Projects Manager',
        'Projects User'
    ],
    'on_setup': 'erpnext.projects.setup.setup_projects',
    'remove_dashboard': 'erpnext.projects.setup.remove_dashboard'
}