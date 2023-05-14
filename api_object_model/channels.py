from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response

class Channels(RootApi):
    """
    Channels object wrapper with all useful methods to interact with ...
    """

    def __init__(self) -> None:
        super().__init__()

    def list_active_channels(self, nodeIndex):
        """
        Lists all active channels between this node and other nodes on the Hopr network. By default response will contain all
        incomming and outgoing channels that are either open, waiting to be opened, or waiting to be closed.
        If you also want to receive past channels that were closed, you can pass includingClosed in the request url query.
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.CHANNELS_ACTIVE_CHANNEL_LIST)
        restService = restApiService.RestApiService(self.get_auth_token())
        response: Response = restService.get_request(url)
        if response.status_code == 200:
            print(response.json())
        else:
            self.handle_http_error(response)

    def other_utility_method_around_these_APIs(self) -> None:
        """
        """
        pass