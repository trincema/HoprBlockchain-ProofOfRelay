import requests
import api_object_model.root_api as rootApi
import services.rest_api_service as restApiService
from requests import Response

class RestApiService(rootApi.RootApi):
    """
    Wrapper utility class over Python requests library used to handle REST API calls
    """

    def __init__(self, authToken) -> None:
        self.authToken = authToken
        self.headers = {
            "X-Auth-Token": self.authToken,
            'Connection': 'close'
        }
    
    def set_headers(self, headers) -> None:
        """
        """
        self.headers = headers
    
    def get_request(self, nodeIndex: int, path: str) -> object:
        """
        Making a REST GET request and returning the 'Response' object to the caller.
        :return: Request data
        """
        url = self.get_rest_url(nodeIndex, path)
        response: Response = requests.get(url, headers=self.headers)
        if response.status_code >= 200 and response.status_code < 300:
            # Tickets statistics fetched successfully.
            data = response.json()
            return data
        else:
            self.handle_http_error(response)
    
    def post_request(self, url, payload) -> Response:
        """
        Making a REST GET request and returning the 'Response' object to the caller.
        """
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def put_request(self, url, payload):
        """
        """
        response = requests.put(url, data=payload, headers=self.headers)
        return response