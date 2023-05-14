import api_object_model.node as node
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import api_object_model.channels as channels
import api_object_model.root_api as rootApi

"""
POST /messages/
Send a message to another peer using a given path (list of node addresses that should relay our message through network).
If no path is given, HOPR will attempt to find a path.
Functional Scenario:
1. If we provide correct values for both 'path' and 'hops', the message should de sent, and 'hops' should be ignored
2. If we provide correct values for 'hops' and leave hops empty (or out) the message should be sent successfully
Boundary Value Analysis - It is clear that body and recipient parameters are mandatory, but:
1. What happens if 'path' and 'hops' parameters are both missing? (what status code should we expect?)
2. What happens if we only provide to the API body an empty 'path' list?
3. What happens if we only provide to the API body a 'hops' parameter with 0 value?
4. What happens if we only provide to the API body a 'hops' parameter with 1 value?
5. What is the maximum number of hops one can set?
6. What is the maximum number of 'path's one can set? The maximum POST request body size is configured on the HTTP server
and typically ranges from 1MB to 2GB. So, its a lot of paths, what are the business scenarios here?
7. What is the maximum number of characters a message can have?
As a QA engineer I would make some experiments here, learn some new things about the product/system, generate new ideas
and questions in my head, discuss them with neccesarry stakeholders and see about further steps.
These basic questions provide valuable insight for the development of Integration, System, Performance, and End-to-End Test Scenarios.
"""

def test_case1():
    """
    /messages/ Should return 202 if both path and hops parameters are set.
    The message should be sent successfully. NOTE: This does not imply successful delivery.
    """
    nodeInstance = node.Node()
    for i in range(1, 6):
        peerId = nodeInstance.get_peer_id(i)
        print("node{}: {}".format(i, peerId))
    channelsInstance = channels.Channels()
    for nodeIndex in range(1, 6):
        channelsInstance.list_active_channels(nodeIndex)

    recipient = nodeInstance.get_peer_id(2)
    path = nodeInstance.get_peer_id(3)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        "path": [
            path
        ],
        "hops": 1
    }
    print(body)
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    print("Response: {} status: {}".format(response.json(), response.status_code))
    if response.status_code != 202:
        root = rootApi.RootApi()
        root.handle_http_error(response)

def test_case2():
    """
    /messages/ Should return 202 if 'hops' parameter is set with a valid value. 'path' can be empty list
    The message should be sent successfully. NOTE: This does not imply successful delivery.
    """
    nodeInstance = node.Node()
    recipient = nodeInstance.get_peer_id(2)
    path = nodeInstance.get_peer_id(3)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        "path": [],
        "hops": 1
    }
    print(body)
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    print("Response: {} status: {}".format(response.json(), response.status_code))
    if response.status_code != 202:
        root = rootApi.RootApi()
        root.handle_http_error(response)

def xtest_case1():
    """
    Should return 422 if path and hops parameters are missing.
    The message should not be sent at this point.
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
    print("Response: {} status: {}".format(response.json(), response.status_code))
    assert response.status_code == 422
    assert response.json()['error'] == 'Failed to find automatic path'

def xtest_case2():
    """
    /messages/ Should return 202 if hops parameter is missing.
    The message should be sent successfully. NOTE: This does not imply successful delivery.
    """
    nodeInstance = node.Node()
    recipient = nodeInstance.get_peer_id(2)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        "path": []
    }
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    print("Response: {} status: {}".format(response.json(), response.status_code))
    assert response.status_code == 202

def xtest_case3():
    """
    /messages/ Should return 400 if path is missing.
    The message should not be sent in this case.
    """
    nodeInstance = node.Node()
    recipient = nodeInstance.get_peer_id(2)
    body = {
        "body": "Hello from future",
        "recipient": recipient,
        "hops": 0
    }
    url = 'http://localhost:13301/api/v2/{}'.format(urls.Urls.MESSAGES_SEND)
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())
    response: Response = restService.post_request(url, body)
    print("Response: {} status: {}".format(response.json(), response.status_code))
    assert response.status_code == 400
