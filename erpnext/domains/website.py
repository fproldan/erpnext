from __future__ import unicode_literals

data = {
    'modules': [
        'Website'
    ],
    'restricted_roles': [
        'Website Manager',
        'Knowledge Base Contributor',
        'Knowledge Base Editor',
        'Blogger'
    ],
    'on_setup': 'frappe.website.setup.setup_website',
}
