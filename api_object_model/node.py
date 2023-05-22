from .root_api import RootApi
from .account import Account, Address
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import streamtologger
import json
import time

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
        account  = Account()
        return account.get_address(nodeIndex, Address.HOPR)
    
    def get_announced_last_seen(self, nodeIndex, peerId) -> int:
        """
        Get the last time the node that was visited by the hop
        It seems in the CI there takes some time until the node is marked as visited by the hop,
        so a waiting mechanism is impplemented to retry the API call until we have the node visited by the hop.
        :nodeIndex: The index of the node to check the last seen attribute
        :peerId: The peer that announced itself to the node
        :return: 
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        while True:
            data = restService.get_request(nodeIndex, urls.Urls.NODE_PEER_LIST)
            print("Response: {}".format(json.dumps(data)))
            found = False
            lastSeenList = data["announced"]
            for lastSeen in lastSeenList:
                if lastSeen['peerId'] == peerId:
                    found = True
                    return int(lastSeen['lastSeen'])
            if found == True:
                break
            time.sleep(5)
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

    def get_node_info(self, nodeIndex: int):
        """
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.NODE_INFO)
        print(data)