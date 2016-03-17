from flask import request, current_app
from app.utils import set_if_not_none
from geojson import Point

GEONAMES = 'http://sws.geonames.org/{}'


def save_ip_of_request(prove_usages: list):
    for prove_usage in prove_usages:
        prove_usage['ip'] = request.remote_addr
        response = current_app.geoip(request.remote_addr)
        if response.city.name is not None:
            prove_usage['city'] = {
                '@type': 'City',
                'confidence': response.city.confidence,
                'sameAs': GEONAMES.format(response.city.geoname_id),
                'name': response.city.name
            }
        if response.continent.name is not None:
            prove_usage['continent'] = {
                '@type': 'Continent',
                'sameAs': GEONAMES.format(response.continent.geoname_id),
                'geoipCode': response.continent.code,
                'name': response.continent.name
            }
        if response.country.name is not None:
            prove_usage['country'] = {
                '@type': 'Country',
                'sameAs': GEONAMES.format(response.country.geoname_id),
                'isoCode': response.country.iso_code,
                'name': response.country.name,
                'confidence': response.country.confidence
            }
        if response.location.latitude is not None:
            prove_usage['geo'] = Point((response.location.latitude, response.location.longitude))
            prove_usage['geo']['accuracy'] = response.location.accuracy_radius
        subdivision = response.subdivisions[-1]
        prove_usage['administrativeArea'] = {
            '@type': 'AdministrativeArea',
            'sameAs': GEONAMES.format(subdivision.geoname_id),
            'confidence': subdivision.confidence,
            'isoCode': subdivision.iso_code,
            'name': subdivision.name
        }
        set_if_not_none(prove_usage, 'isp', response.traits.isp)
        set_if_not_none(prove_usage, 'organization', response.traits.organization)
        set_if_not_none(prove_usage, 'userType', response.traits.user_type)
        set_if_not_none(prove_usage, 'autonomousSystemNumber', response.traits.autonomous_system_number)
