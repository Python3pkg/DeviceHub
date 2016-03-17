import copy

from app.event.settings import event_sub_settings_one_device, event_with_one_device, place
from app.place.schema import country, city, continent, administrative_area

prove_usage = copy.deepcopy(event_with_one_device)
prove_usage.update(copy.deepcopy(place))
prove_usage_settings = copy.deepcopy(event_sub_settings_one_device)

prove_usage.update({
    'ip': {
        'type': 'string',
        'readonly': True
    },
    'country': {
        'type': 'dict',
        'schema': country,
        'readonly': True
    },
    'administrativeArea': {
        'type': 'dict',
        'schema': administrative_area,
        'readonly': True
    },
    'city': {
        'type': 'dict',
        'schema': city,
        'readonly': True
    },
    'continent': {
        'type': 'dict',
        'schema': continent,
        'readonly': True
    },
    'isp': {
        'type': 'string',
        'readonly': True
    },
    'organization': {
        'type': 'string',
        'readonly': True
    },
    'userType': {
        'type': 'string',
        'readonly': True
    },
    'autonomousSystemNumber': {
        'type': 'natural',
        'readonly': True
    }
})

prove_usage_settings.update({
    'schema': prove_usage,
    'url': event_sub_settings_one_device['url'] + 'prove-usage',

})
prove_usage_settings['datasource']['filter'] = {'@type': {'$eq': 'ProveUsage'}}
