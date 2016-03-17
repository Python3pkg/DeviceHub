import pymongo

from app.place.schema import place

place_settings = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE', 'PUT'],
    'schema': place,
    'datasource': {
        'default_sort': [('_created', -1)]
    },
    'extra_response_fields': ['devices'],
    'url': 'places',
    'mongo_indexes': {
        'geo': [('components', pymongo.GEO2D)],
    }
}
