from websocket import create_connection
from websocket import WebSocketTimeoutException
import api_object_model.root_api as rootApi

class WebsocketClientService(rootApi.RootApi):
    """
    Websocket client wrapper service with the purpose to manage one websocket client connection.
    """

    def __init__(self) -> None:
        pass

    def create_client_connection(self, nodeIndex, path, timeout = 30) -> None:
        """
        Open a new websocket client connection to the given URL
        """
        wsUrl = self.get_ws_url(nodeIndex, path)
        print("wsUrl = {}".format(wsUrl))
        self.webSocket = create_connection(wsUrl, timeout)
    
    def receive_message(self):
        """
        Blocking operation. Wait for a message and return it to the caller when received.
        """
        message = self.webSocket.recv()
        return message

    def close_client_connection(self):
        """
        Closing the current websocket client connection in a safe way.
        """
        try:
            self.webSocket.close()
        except WebSocketTimeoutException:
            pass