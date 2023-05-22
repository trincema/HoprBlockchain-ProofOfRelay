from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response

class Tokens(RootApi):
    def __init__(self):
        pass

    def get_token(self, nodeIndex) -> str:
        """
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.TOKENS_FULL_TOKEN_INFO)
        return data['id']

    def create_new_authentication_token(self):
        """
        """
        pass