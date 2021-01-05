from flask_site.captioning_api.captioning_api_v2_dispatch.input_verifiers import verifier as verification
import flask_site.captioning_api.captioning_api_v2_dispatch.request_errors as error
from flask_site.captioning_api.captioning_api_v2_dispatch.response_serializer import SerializerMixin


class BaseRequest(SerializerMixin, object):

    def __init__(self, payload,  resource, query_string = None):

        self.payload = payload
        self.resource = resource.split("/")[-1]
        self.query_string = query_string
        self.verifier = verification[self.resource](self.payload)
        self.verified = None
        self.response_code = 200
        self.database_query = None
        self.serialized_query = None
        self.message = None
        self.headers = None
        self.error = None
        self.return_payload = None


    def verify_keys(self, method_type):

        self.verified = self.verifier.__getattribute__(method_type)

        if not self.verified:
            error_state = error.QueryKeyDoesNotExist
            self.error = error_state("Key passed can't be used to query database", 405)
            self.response_code = self.error.status_code

    def assign_request_query(self, query):

        self.database_query = query.returned

        if self.__class__.__name__ == 'AddObject':
            if query.already_exists:
                self.response_code = 200
        return True

    def serialize_query(self, primary_key):

        if isinstance(self.database_query, tuple): # Write returns a tuple if success or not

            if self.error is None:
                self.serialized_query = {"status": True, "echo": self.database_query[2]}
            else:
                self.serialized_query = {"status": False}
        else:

            self.serialized_query = self.serialize(self.resource, self.database_query, primary_key)


class AddObject(BaseRequest):

    def __init__(self, payload, query_string, resource):
        BaseRequest.__init__(self, payload, resource, query_string)
        self.verify_keys("post_valid")
        self.response_code = 201

class UpdateObject(BaseRequest):

    def __init__(self, payload, query_string, resource):
        BaseRequest.__init__(self, payload, resource, query_string)
        self.verify_keys("put_valid")


class GetObject(BaseRequest):

    def __init__(self,  payload,  resource ):
        BaseRequest.__init__(self, payload, resource)
        self.verify_keys("query_valid")


