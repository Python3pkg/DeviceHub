from flask import request, current_app
from app.utils import set_if_not_none


def save_ip_of_request(prove_usages: list):
    for prove_usage in prove_usages:
        prove_usage['ip'] = request.remote_addr
        response = current_app.geoip(request.remote_addr)
        set_if_not_none(prove_usage, 'country', response.country.iso_code)
        set_if_not_none(prove_usage, 'subdivision', response.subdivisions.most_specific.iso_code)
        set_if_not_none(prove_usage, 'city', response.city.name)
        set_if_not_none(prove_usage, 'postal_code', response.postal.code)
        set_if_not_none(prove_usage, 'latitude', response.location.latitude)
        set_if_not_none(prove_usage, 'longitude', response.location.longitude)
        



