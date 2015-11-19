import copy

from app.utils import register_sub_types, normalize
from app.schema import thing

HID_REGEX = '[\w]+-[\w]+'

product = dict(thing, **{
    'model': {
        'type': 'string'
    },
    'weight': {  # In kilograms
                 'type': 'float',
                 },
    'width': {  # In meters
                'type': 'float'
                },
    'height': {  # In meters
                 'type': 'float'
                 },
    'manufacturer': {
        'type': 'string',
        'coerce': normalize,
    },
    'productId': {
        'type': 'string'
    },
})

individualProduct = dict(product, **{
    'serialNumber': {
        'type': 'string',
        'coerce': normalize,
    }
})

device = copy.deepcopy(individualProduct)
device.update({
    '_id': {
        'type': 'string',
        'unique': True
    },
    'hid': {
        'type': 'string',
        'regex': HID_REGEX  # unique breaks other resources
    },
    'isUidSecured': {
        'type': 'boolean'
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'devices',
                'embeddable': True,
                'field': '_id'
            }
        },
        'default': []
    }
})

device_settings = {
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'schema': device,
    'additional_lookup': {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    },
    'embedded_fields': ['components'],
    'url': 'devices'
}

device_sub_settings = {
    'resource_methods': ['POST'],
    'item_methods': ['DELETE'],
    'url': device_settings['url'] + '/',
    'datasource': {
        'source': 'devices'
    },
    'embedded_fields': device_settings['embedded_fields'],
    'extra_response_fields': ['@type']
}


def register_parent_devices(domain: dict):
    return register_sub_types(domain, 'app.device', ('Computer',))
