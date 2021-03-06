class Translator:
    def __init__(self, config: dict, **kwargs):
        self.config = config
        self.database = None

    def translate(self, resource_or_resources: list or dict, database: str = None) -> list:
        """
        Translates a resource or a group of resources.
        :param database: The database in DeviceHub (i.e. db1)
        :param resource_or_resources: The data to translate
        :return: A list of tuples, containing 1. the translated resource, 2. the original resource
        """
        self.database = database
        return [(self._translate(resource_or_resources), resource_or_resources)]

    def _translate(self, resource_or_resources: list or dict) -> dict:
        """
        Translates a resource. This method carries the actual translation.
        :param resource:
        :return: The translated resource
        """
        raise NotImplementedError()


class ResourceTranslator(Translator):
    """
        Translates (or transforms) the structure of a resource to adequate it to another agent.

        Translation is done by specifying a translation dictionary, which is used to change from
        an original resource to the final one.
        Every field of the translation dict contains a method used to transform the original value from
        DeviceHub to the final one. Translator comes with some transformers, and subclass it to add more.

        Translation dictionaries are as follows:
        For generic translation dict: ['final_field_name'] = (transformer_method, 'original field name')
        For specific translation dicts:
            ['resource type name']['final field name'] = (transformer_method, 'original field name')
        Where 'final field name' is the name of the field in the agent, 'original field name' is the field name
        in DeviceHub (only add it if final name and original name differ), transformer_method is one of the transformer
        methods in Translator, and 'resource type name' e.g. devices:Register.
        See :func `GRDTranslator.__init__`: for an example.
    """

    def __init__(self, config, generic_dict: dict = None, specific_dict: dict = None, **kwargs):
        """
        Configures the translator. Once done, you can translate many resources as you want with :py:meth:`.translate`:.
        :param config:
        :param generic_dict: Generic translation dictionary shared among resources.
        :param specific_dict: Specific translation dictionary divided per resource.
        """
        self.config = config
        self.generic_dict = generic_dict
        self.specific_dict = specific_dict or {}
        super().__init__(config, **kwargs)

    def _translate(self, resource: dict) -> dict:
        """
        Translates a resource. This method carries the actual translation.
        :param resource:
        :return: The translated resource
        """
        translated = dict()
        fields = list(dict(self.generic_dict, **self.specific_dict.get(resource['@type'], {})).items())
        for final_name, (method, *original_name) in fields:
            value = resource.get(original_name[0] if len(original_name) > 0 else final_name)
            if value is not None:
                translated[final_name] = method(value)
        return translated

    # Transformers
    def url(self, resource_name: str):
        """Obtains an url from the resource identifier.
        :param resource_name: full resource-name with the prefix, if needed it.
        """

        def url(resource_or_identifier):
            try:
                return self._get_resource_url(resource_or_identifier['_id'], resource_name)
            except TypeError:
                return self._get_resource_url(resource_or_identifier, resource_name)

        return url

    @staticmethod
    def for_all(method):
        """Executes a transformer method for each value and returns a list of results"""

        def _loop(values: list) -> list:
            return [method(value) for value in values]

        return _loop

    @staticmethod
    def identity(value):
        """Returns the same value."""
        return value

    def device(self, device: dict) -> dict:
        """Obtains the device"""
        return device

    def hid_or_url(self, device: dict):
        """Returns HID if exists, or the URL of the device otherwise."""
        return device.get('hid', self._get_resource_url(device['_id'], 'devices'))

    # Helpers
    def _get_resource_url(self, identifier, resource_name: str):
        if self.config['DOMAIN'][resource_name]['use_default_database']:
            url = '{}/{}'.format(resource_name, identifier)
        else:
            url = '{}/{}/{}'.format(self.database, resource_name, identifier)
        return self._parse_url(url)

    def _parse_url(self, url):
        if self.config['URL_PREFIX']:
            url = '{}/{}'.format(self.config['URL_PREFIX'], url)
        return self.config['BASE_URL_FOR_AGENTS'] + '/' + url

    @staticmethod
    def inner_field(field: str):
        """Gets a field that is one level nested in a dict"""

        def _inner_field(value: dict):
            return value[field]

        return _inner_field

    @staticmethod
    def inner_fields(fields: list, concat=' '):
        """Gets and concats the inner fields"""

        def _inner_fields(value: dict):
            result = ''
            for i, field in enumerate(fields):
                result += value.get(field, '')
                if i != len(fields) - 1:
                    result += concat
            return result

        return _inner_fields

    @staticmethod
    def inner_resource(resource_type: str, after=identity):
        """Gets an entire inner resource, or optionally some of its fields"""

        def _inner_resource(resources: list):
            resource, *_ = [resource for resource in resources if resource['@type'] == resource_type]
            return after(resource)

        return _inner_resource

    @staticmethod
    def nth_resource(nth: int, after=identity):
        """Gets the nth resource"""

        def _nth_resource(resources: list):
            return after(resources[nth])

        return _nth_resource


class ResourcesTranslator(Translator):
    def __init__(self, config: dict, resource_translator: ResourceTranslator, generic_dict: dict = None,
                 specific_dict: dict = None, **kwargs):
        self.config = config
        self.resource_translator = resource_translator
        self.generic_dict = generic_dict
        self.specific_dict = specific_dict
        super().__init__(config, **kwargs)

    def _translate_resources(self, resources: list) -> list:
        return [self.resource_translator.translate(resource)[0] for resource in resources]

    def _translate(self, resources: list) -> dict:
        raise NotImplementedError()
