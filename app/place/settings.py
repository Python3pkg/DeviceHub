import copy
from app.schema import thing

__author__ = 'Xavier Bustamante Talavera'

place = copy.deepcopy(thing)
place.update({
    'geo': {
        'type': 'polygon'
    },
    'type': {
        'type': 'string',
        'allowed': ['Department', 'Zone', 'Warehouse', 'CollectionPoint']
    },
    'devices': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        }
    },
    'description': {
        'type': 'string'
    },
    'byUser': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'readonly': True
    }
})
place['label']['required'] = True

place_settings = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'schema': place,
    'embedded_fields': ['devices', 'parent', 'byUser'],
    'datasource': {
        'default_sort': [('_created', -1)]
    },
    'url': 'places'
}

"""  'children': {  # inner places
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'places',
                'field': '_id',
                'embeddable': True
            }
        }
    },
    'parent': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'places',
            'field': '_id',
            'embeddable': True
        },
        # todo can I be the child of this parent?
    },
"""