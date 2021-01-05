
response_base = {
    'content': None,
    'error': None,
    'request_payload': None,

}


class ResponseObjectBase(object):

    def __init__(self, content=None, error=None, query_obj=None):
        self.response_base = response_base
        self.content = content
        self.query_obj = query_obj
        self.error = error


    def build_response(self):
        self.response_base['content'] = self.content
        self.response_base['request_payload'] = self.query_obj
        self.response_base['error'] = self.error

    def __call__(self):
        return self.response_base


class ContentResponse(ResponseObjectBase):

    def __init__(self, content):
        ResponseObjectBase.__init__(self)
        self.content = content
        self.build_response()


class ErrorResponse(ResponseObjectBase):

    def __init__(self, error, query_obj):
        ResponseObjectBase.__init__(self)
        self.error = error.to_dict()
        self.query_obj = query_obj
        self.build_response()