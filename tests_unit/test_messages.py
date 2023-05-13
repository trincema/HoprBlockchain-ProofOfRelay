import api_object_model.node as node
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import api_object_model.channels as channels

def test_case1():
    """
    """
    nodeInstance = node.Node()
    recipient = nodeInstance.get_peer_id(2)
    body = {
        "body": "Hello from future",
        "recipient": recipient
    }
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    assert response.status_code == 422
    assert response.json()['error'] == 'Failed to find automatic path'

def test_case2():
    """
    """
    nodeInstance = node.Node()
    for i in range(1, 6):
        peerId = nodeInstance.get_peer_id(i)
        print("node{}: {}".format(i, peerId))
    channelsInstance = channels.Channels()
    for nodeIndex in range(1, 6):
        channelsInstance.list_active_channels(nodeIndex)

    nodeInstance = node.Node()
    recipient = nodeInstance.get_peer_id(2)
    path = nodeInstance.get_peer_id(3)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        path: [path]
    }
    print(body)
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    print("Error: {}".format(response.json()['error']))
    assert response.status_code == 202
    # assert response.json()['error'] == 'Failed to find automatic path'