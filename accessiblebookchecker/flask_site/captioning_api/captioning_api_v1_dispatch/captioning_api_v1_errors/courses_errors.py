from flask import jsonify


class InvalidParams:
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        self.error_class = "Invalid Params"
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv




class NoResultsFound:

    status_code = 404

    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        self.error_class = "No Results Found"
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidDataTypes:
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        self.error_class = "Invalid Data Type"
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class IntegrityError:
    status_code = 409

    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        self.error_class = "Integrity Error, Key Not Found"
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
