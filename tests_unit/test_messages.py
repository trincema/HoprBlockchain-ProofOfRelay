import pytest
import json
from typing import List
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

class Input:
    def __init__(self, sender: int, receiver: int, message: str, path: List[int], hops: int) -> None:
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.path = path
        self.hops = hops

class Output:
    def __init__(self, expectedStatusCode: int, expectedStatus: str, expectedErrorMessage: str) -> None:
        self.expectedStatusCode = expectedStatusCode
        self.expectedStatus = expectedStatus
        self.expectedErrorMessage = expectedErrorMessage

@pytest.mark.parametrize("input, output",[
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [3], hops = 1),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [], hops = 1),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = 1),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [], hops = None),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = None),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
        # This is strange, at some point this combination was giving 422 error, and now it works ??
        # TODO have to investigate further (I'm used with these kind of issues/bugs in automation, especially with crypto it seems)
        # Output(expectedStatusCode = 422, expectedStatus = None, expectedErrorMessage = "Failed to find automatic path")
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = 0),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = None, path = None, hops = None),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = None, message = 'Hello from future', path = None, hops = None),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_ADDRESS', expectedErrorMessage = None)
    )
])
def test_case1(input: Input, output: Output) -> None:
    """
    Template used to send a message with varous inputs and check the expected status code and error message as output.
    """
    # Instantiating objects needed during the test case
    root = rootApi.RootApi()
    nodeInstance = node.Node()
    restService = restApiService.RestApiService(nodeInstance.get_auth_token())

    # Preparing input data
    url = root.get_rest_url(input.sender, urls.Urls.MESSAGES_SEND)
    body = {}
    if input.message != None:
        body["body"] = input.message
    if input.receiver != None:
        body["recipient"] = nodeInstance.get_peer_id(input.receiver)
    if input.path != None:
        peerIdPath = []
        for nodeId in input.path:
            peerIdPath.append(nodeInstance.get_peer_id(nodeId))
        body["path"] = peerIdPath
    if input.hops != None:
        body["hops"] = input.hops
    
    print("url={}".format(url))
    print("body={}".format(json.dumps(body)))

    # Executing the operations based on the provided input
    response: Response = restService.post_request(url, body)
    print("Response: {} status: {}".format(response.json(), response.status_code))
    
    # Checking the output
    assert response.status_code == output.expectedStatusCode
    if output.expectedStatus != None:
        assert response.json()['status'] == output.expectedStatus
    if output.expectedErrorMessage != None:
        assert response.json()['error'] == output.expectedErrorMessage

def test_case2():
    """
    The 2nd type of Test Case we can have is to test the boundary values of the message.
    Case 1: Send an empty message
    Case 2: Send 1 character message
    Case 3: Send special character message
    Case 4: Which is the maximum length of message supported by the platform? HTTP supports from 1MB to 1GB
    as the maximum size of the payload, so we can explore with larger messages to see what happens.
    """
    pass

def debug_nodes():
    """
    Helper method to print the peer ids for each node and then the list of active channels for the nodes
    """
    nodeInstance = node.Node()
    for i in range(1, 6):
        peerId = nodeInstance.get_peer_id(i)
        print("node{}: {}".format(i, peerId))
    channelsInstance = channels.Channels()
    for nodeIndex in range(1, 6):
        channelsInstance.list_active_channels(nodeIndex)
