from eve.auth import requires_auth
from flask import jsonify
from flask import request

from app.aggregation.aggregation import Aggregation, AggregationError
from app.app import app
from app.flask_decorators import crossdomain, cache


@app.route('/<db>/aggregations/<resource>/<method>', methods=['GET'])
@cache(Aggregation.CACHE_TIMEOUT)
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def aggregate_view(db, resource, method):
    aggregation = Aggregation(resource)
    if method == '_aggregate':
        raise AggregationError("You cannot use _aggregate.")
    try:
        m = getattr(aggregation, method)(request.args)
    except AttributeError as a:
        raise AggregationError(a.args)
    else:
        return jsonify(m)
