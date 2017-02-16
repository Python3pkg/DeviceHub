import copy

import iso3166
import pymongo

from ereuse_devicehub.resources.group.physical.settings import Physical, PhysicalSettings
from ereuse_devicehub.resources.group.settings import places_fk, lots_fk, packages_fk, \
    devices_fk


class Place(Physical):
    geo = {
        'type': 'polygon',
        'sink': -5,
        'description': 'Set the area of the place. Be careful! Once set, you cannot update the area.',
        'modifiable': False
    }
    type = {
        'type': 'string',
        'allowed': {'Department', 'Zone', 'Warehouse', 'CollectionPoint'}
    }
    ancestors = copy.deepcopy(Physical.ancestors)
    ancestors['schema']['schema']['places'] = places_fk
    children = copy.deepcopy(Physical.children)
    children['schema']['packages'] = packages_fk
    children['schema']['lots'] = lots_fk
    children['schema']['devices'] = devices_fk
    children['schema']['places'] = places_fk
    children['schema']['components'] = devices_fk
    address = {
        'type': 'dict',
        'schema': {
            'addressCountry': {
                'type': 'string',
                'allowed': {key for key in iso3166.countries_by_alpha2},
                'description': 'The name of the country',
                'doc': 'The addressCountry as per ISO 3166 (2 characters).'
            },
            'addressLocality': {
                'type': 'string',
                'description': 'The locality. For example, Barcelona.'
            },
            'addressRegion': {
                'type': 'string',
                'description': 'The region. For example, CA.'
            },
            'postalCode': {
                'type': 'string',
                'description': 'The postal code. For example, 94043.'
            },
            'streetAddress': {
                'type': 'string',
                'description': 'The street address. For example, C/Jordi Girona, 1-3.'
            }
        }
    }
    telephone = {
        'type': 'string'
    }


class PlaceSettings(PhysicalSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Place
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'places'
    }
    mongo_indexes = {
        'geo': [('components', pymongo.GEO2D)]
    }
    url = 'places'
