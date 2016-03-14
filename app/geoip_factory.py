from geoip2 import webservice


class GeoIPFactory:
    def __init__(self, settings):
        if settings.GEO_IP_USE_WEB_SERVICE:
            self.client = webservice.Client(settings.MAX_MIND_ACCOUNT['user'], settings.MAX_MIND_ACCOUNT['license key'])

    def __call__(self, data):
        if 'client' in self:
            return self.client.insights(data)