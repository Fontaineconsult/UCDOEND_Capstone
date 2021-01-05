


class NoRouteExistsForMethod(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None, exception = None):
        Exception.__init__(self)
        self.message = message
        self.error_class = exception
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv["error_message"] = self.message
        return rv



class QueryKeyDoesNotExist(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None, exception = None):
        Exception.__init__(self)
        self.message = message
        self.error_class = "Key Doesn't Exist"
        if status_code is not None:
            self.status_code=status_code
        self.payload = payload


    def to_dict(self):
        rv = dict(self.payload or ())
        rv["error_message"] = self.message
        return rv

