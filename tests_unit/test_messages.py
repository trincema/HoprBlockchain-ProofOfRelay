import api_object_model.node as node
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import time

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
    recipient = nodeInstance.get_peer_id(2)
    path = nodeInstance.get_peer_id(3)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        path: [path]
    }
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    assert response.status_code == 202
    # assert response.json()['error'] == 'Failed to find automatic path'