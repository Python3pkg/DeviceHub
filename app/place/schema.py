import copy

from app.schema import thing

schema_place = copy.deepcopy(thing)

city = copy.deepcopy(schema_place)
city.update({
    'confidence': {
        'type': 'natural'
    }
})

country = copy.deepcopy(schema_place)
country.update({
    'confidence': {
        'type': 'natural'
    },
    'isoCode': {
        'type': 'string',
        'description': 'The ISO Code as ISO 3166-1'
    }
})

administrative_area = copy.deepcopy(schema_place)
administrative_area.update({
    'confidence': {
        'type': 'natural'
    },
    'isoCode': {
        'type': 'string',
        'description': 'The ISO Code as ISO 3166-1'
    }
})

continent = copy.deepcopy(schema_place)
continent.update({
    'geoipCode': {
        'type': 'string',
        'description': 'The GEOIP Code'
    }
})

place = copy.deepcopy(schema_place)
place.update({
    'geo': {
        'type': 'polygon',
        'sink': -5,
        'description': 'Set the area of the place. Be careful! Once set, you cannot update the area.',
        'modifiable': False
    },
    'type': {
        'type': 'string',
        'allowed': ['Department', 'Zone', 'Warehouse', 'CollectionPoint']
    },
    'devices': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'default': [],
        'unique_values': True
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
place['@type']['allowed'] = ['Place']