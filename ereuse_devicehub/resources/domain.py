from bson.objectid import ObjectId
from ereuse_devicehub.exceptions import Exception
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.utils import ClassProperty
from flask import current_app


class Domain:
    """Provides utility methods to work with resources, like easier access to data-layers. Extend it happily."""
    resource_settings = ResourceSettings
    """Link to the resource settings. Override it linking it with the appropriate subclass"""

    @classmethod
    def get_one(cls, id_or_filter: dict or ObjectId or str):
        """
        Obtains a resource.
        :param id_or_filter: An identifier or the filter in Mongo to obtain the resource.
        :throws ResourceNotFound:
        :return:
        """
        resource = current_app.data.find_one_raw(cls.source, id_or_filter)
        if resource is None:
            if type(id_or_filter) is dict:
                text = 'There is no resource matching the query {}'.format(id_or_filter)
            else:
                text = 'The resource with id {} does not exist.'.format(id_or_filter)
            raise ResourceNotFound(text)
        else:
            return resource

    @classmethod
    def get(cls, query_filter: dict) -> list:
        """
        Obtains several resources.
        :param query_filter: A Mongo filter to obtain the resources.
        """
        return list(current_app.data.find_raw(cls.source, query_filter))

    @classmethod
    def update_raw(cls, ids: str or ObjectId or list, operation: dict):
        """
        Sets the properties of a resource using directly the database layer.
        :param ids:
        :param operation: MongoDB update query.
        :return The number of files edited in total
        """
        resources_id = [ids] if type(ids) is str or type(ids) is ObjectId else ids
        count = 0
        for resource_id in resources_id:
            count += current_app.data.driver.db[cls.source].update_one({'_id': resource_id}, operation).modified_count
        return count

    @classmethod
    def update_many_raw(cls, filter, operation):
        return current_app.data.driver.db[cls.source].update_many(filter, operation)

    @classmethod
    def update_one_raw(cls, resource_id: str or ObjectId, operation):
        count = current_app.data.driver.db[cls.source].update_one({'_id': resource_id}, operation).matched_count
        if count == 0:
            name = cls.resource_settings._schema.type_name
            raise ResourceNotFound('{} {} cannot be updated as it is not found.'.format(name, resource_id))

    @classmethod
    def delete(cls, query):
        return current_app.data.driver.db[cls.source].delete_one(query)

    # noinspection PyNestedDecorators
    @ClassProperty
    @classmethod
    def source(cls):
        try:
            return cls.resource_settings.datasource['source']
        except AttributeError:
            raise AttributeError('Make sure resource_settings points to the correct subclass of ResourceSettings.')

    @classmethod
    def path_for(cls, database: str, identifier: str or ObjectId or int) -> str:
        """Returns the resource path for a given identifier."""
        path = current_app.config['DOMAIN'][cls.resource_settings.resource_name()]['url']
        return '{}/{}/{}'.format(database, path, str(identifier))

    @classmethod
    def url_agent_for(cls, database: str, identifier: str or ObjectId or int):
        """Returns the resource full url as seen for other agents."""
        return '{}/{}'.format(current_app.config['BASE_URL_FOR_AGENTS'], cls.path_for(database, identifier))


class ResourceNotFound(Exception):
    status_code = 422
