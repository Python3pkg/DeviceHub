import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device
from app.validation import IF_VALUE_REQUIRE

test_hard_drive = copy.deepcopy(event_with_one_device)
test_hard_drive_settings = copy.deepcopy(event_sub_settings_one_device)
test_hard_drive.update({
    'type': {
        'type': 'string',
        # 'allowed': ['Short offline', 'Extended offline'],
        # 'required': True
    },
    'status': {
        'type': 'string',
        'required': True
    },
    'lifetime': {
        'type': 'integer',
    },
    'firstError': {
        'type': 'integer',
        'nullable': True
    },
    'snapshot': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'field': '_id',
            'embeddable': True
        }
    },
    'error': {
        'type': 'boolean',
        'required': True,
        # IF_VALUE_REQUIRE: (False, ('type', 'lifetime', 'firstError')) todo this can just be done when hard-drive is not
        # nested, so we will be able to activate it when, in snapshot, we can abort TestHardDrive event
    }
})
test_hard_drive_settings.update({
    'schema': test_hard_drive,
    'url': event_sub_settings_one_device['url'] + 'test_hard_drive'
})
test_hard_drive_settings['datasource']['filter'] = {'@type': {'$eq': 'TestHardDrive'}}