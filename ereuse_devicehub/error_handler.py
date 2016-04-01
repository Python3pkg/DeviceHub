from flask import Response, redirect as flask_redirect, current_app, request
from flask.json import jsonify

from ereuse_devicehub.app import app
from ereuse_devicehub.exceptions import BasicError, Redirect
from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.utils import get_header_link


@app.errorhandler(BasicError)
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def handle_standard_error(error: BasicError) -> Response:
    response = jsonify(error.to_dict())
    header_name, header_value = get_header_link(type(error).__name__)
    response.headers[header_name] = header_value
    response.status_code = error.status_code
    return response


@app.errorhandler(Redirect)
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def redirect(error: Redirect):
    """
    Returns flask.redirect, performing a redirection to the client
    :param error:
    :return: Response
    """
    return flask_redirect(current_app.config['CLIENT'] + request.full_path)