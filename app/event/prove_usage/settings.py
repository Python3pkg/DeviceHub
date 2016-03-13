import copy

from app.event.settings import event_sub_settings_one_device, event_with_one_device, place

prove_usage = copy.deepcopy(event_with_one_device)
prove_usage.update(copy.deepcopy(place))
prove_usage_settings = copy.deepcopy(event_sub_settings_one_device)

prove_usage.update({
    'ip': {
        'type': 'string',
        'readonly': True
    }
})

prove_usage_settings.update({
    'schema': prove_usage,
    'url': event_sub_settings_one_device['url'] + 'prove-usage',

})
prove_usage_settings['datasource']['filter'] = {'@type': {'$eq': 'ProveUsage'}}
