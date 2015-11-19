import copy
from app.account.user import Role
from app.device.component.settings import component

from app.event.settings import event_with_one_device, event_sub_settings_one_device
from app.device.computer.settings import computer

snapshot = copy.deepcopy(event_with_one_device)
snapshot.update({
    'offline': {
        'type': 'boolean'
    },
    'automatic': {
        'type': 'boolean'
    },
    'version': {
        'type': 'float',
    },
    'events': {  # Snapshot generates this automatically
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                'embeddable': True,
                'field': '_id'
            }
        },
        'readonly': True
    },
    'request': {  # The request sent, saved in case of debugging
        'type': 'string',
        'readonly': True
    },
    'unsecured': {  # When we match an existing non-hid device, we state it here
        'type': 'list',
        'schema': {
            'type':  'objectid',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'default': [],
        'readonly': True
    },
    'device': {
        'type': 'dict',
        'schema': computer,
        'required': True
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': component
        },
        'default': []
    }
})

snapshot_settings = copy.deepcopy(event_sub_settings_one_device)
snapshot_settings.update({
    'resource_methods': ['POST'],
    'schema': snapshot,
    'url': 'snapshot',
    'get_projection_blacklist': {Role.ADMIN: ('request',)}  # Just superusers
})
snapshot_settings['datasource']['filter'] = {'@type': {'$eq': 'Snapshot'}}
