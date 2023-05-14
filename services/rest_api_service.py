import requests
from requests import Response

class RestApiService:
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
    
    def get_request(self, url) -> Response:
        """
        Making a REST GET request and returning the 'Response' object to the caller.
        """
        response = requests.get(url, headers=self.headers)
        return response
    
    def post_request(self, url, body) -> Response:
        """
        Making a REST GET request and returning the 'Response' object to the caller.
        """
        response = requests.post(url, json=body, headers=self.headers)
        return response