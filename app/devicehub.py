from eve import Eve


class Devicehub(Eve):
    resources_without_different_db = 'accounts',

    def _add_resource_url_rules(self, resource, settings):
        if resource in self.resources_without_different_db:
            super(Devicehub, self)._add_resource_url_rules(resource, settings)
        else:
            real_url_prefix = self.config['URL_PREFIX']
            for database in self.config['DATABASES']:
                self.config['URL_PREFIX'] = database
                super(Devicehub, self)._add_resource_url_rules(resource, settings)
            self.config['URL_PREFIX'] = real_url_prefix