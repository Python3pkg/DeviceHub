from flask import jsonify
from app.app import app

__author__ = 'Xavier Bustamante Talavera'


class StandardError(Exception):
    status_code = 500
    title = 'Unexpected error'
    message = None

    def __init__(self, message=""):
        if self.message is None:
            self.message = self.title + "\n" + message

    def to_dict(self):
        return {'message': self.message, 'title': self.title}


class ValidationError(StandardError):
    status_code = 400
    title = 'Bad Request'
    message = 'The element has not passed validation'


class InnerRequestError(StandardError):
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(message)


class WrongCredentials(StandardError):
    status_code = 401
    title = 'Unauthorized'


class UserIsAnonymous(WrongCredentials):
    pass


class NoPlaceForGivenCoordinates(StandardError):
    status_code = 400
    title = 'Bad Request'
    message = 'There is no place in such coordinates'

class CoordenatesAndPlaceDoNotMatch(StandardError):
    status_code = 400
    title = 'Bad Request'
    message = 'Place and coordenates do not match'

@app.errorhandler(StandardError)
def handle_standard_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
