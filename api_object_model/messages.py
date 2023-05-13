from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
import services.ws_api_service as wsApiService
from requests import Response
from websocket import WebSocketTimeoutException
import json

class Messages(RootApi):
    """
    Messages object wrapper with all useful methods to interact with a certain node addresses, balances, and withdrawals.
    """

    def __init__(self) -> None:
        super().__init__()

    def send_message(self, nodeIndex: int, message: str, recipient: str, path, hops: int) -> None:
        """
        Send a message to another peer using a given path (list of node addresses that should relay our message through network).
        If no path is given, HOPR will attempt to find a path.
        :param nodeIndex The index of the node 
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.MESSAGES_SEND)
        body = {
            "body": message,
            "recipient": recipient
        }
        if len(path) > 0:
            body['path'] = path
        if hops > 0:
            body['hops'] = hops
        print("url={}".format(url))
        print("body={}".format(json.dumps(body)))
        restService = restApiService.RestApiService(self.get_auth_token())
        response: Response = restService.post_request(url, body)
        print("Response: {}".format(response.json()))
        if response.status_code != 200 or response.status_code != 202:
            self.handle_http_error(response)
    
    def check_node_does_not_get_message(self, nodeIndex: int, path: str, timeout: int = 5) -> None:
        """
        Checking that a certain node does not get the message.
        """
        wsUrl = self.get_ws_url(nodeIndex, path)
        webSocket = wsApiService.WebsocketClientService()
        webSocket.create_client_connection(nodeIndex, path, timeout)
        try:
            message = webSocket.receive_message()
            assert 'At least one of the other nodes received the message. Node: {0} Message: {1}'.format(wsUrl, message)
        except WebSocketTimeoutException:
            # Timeout hit, as expected, just close the WS client connection
            webSocket.close_client_connection()