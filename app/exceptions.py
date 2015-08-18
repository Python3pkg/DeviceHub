from flask import jsonify

from DeviceWare import app

__author__ = 'Xavier Bustamante Talavera'


class StandardError(Exception):
    status_code = 500
    title = 'Unexpected error'

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {'message': self.message, 'title': self.title}


class ValidationError(StandardError):
    status_code = 400
    title = 'The element has not passed validation'


@app.errorhandler(StandardError)
def handle_standard_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
