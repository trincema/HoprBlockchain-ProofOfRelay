from requests import Response
from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
import streamtologger

streamtologger.redirect()

class Node(RootApi):
    """
    Node object wrapper with all useful methods to interact with a certain node in the HOPR network.
    """

    def __init__(self):
        pass

    def get_peer_id(self, nodeIndex) -> str:
        """
        Dynamically get the peer ID based on the node index.
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.NODE_INFO)
        restService = restApiService.RestApiService(self.get_auth_token())
        response: Response = restService.get_request(url)
        print("url: {} response: {}".format(url, response.json()))
        if response.status_code == 200:
            # Node information fetched successfuly. Process data and return desired data
            listeningAddress = response.json()["listeningAddress"][0].split('/')
            return listeningAddress[6]
        else:
            # Handle errors according to the Swagger API specs
            self.handle_http_error(response)
    
    def get_announced_last_seen(self, nodeIndex, peerId) -> int:
        """
        Get the last time the node was visited
        :nodeIndex: The index of the node to check the last seen attribute
        :peerId: The peer that announced itself to the node
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.NODE_PEER_LIST)
        restService = restApiService.RestApiService(self.get_auth_token())
        response = restService.get_request(url)

        if response.status_code == 200:
            lastSeenList = response.json()["announced"]
            for lastSeen in lastSeenList:
                if lastSeen['peerId'] == peerId:
                    return int(lastSeen['lastSeen'])
        else:
            # Handle errors according to the Swagger API specs
            self.handle_http_error(response)
        return 0
    
    def not_visited_lately(self, nodeIndex):
        """
        Check that the node vas not visited in the last minute.
        """
        pass

    def visited_lately(self, nodeIndex):
        """
        Check that the node vas visited in the last minute.
        """
        pass