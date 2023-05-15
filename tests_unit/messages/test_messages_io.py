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
        Input(sender = 1, receiver = None, message = None, path = None, hops = None),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = None, path = None, hops = None),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    # 1st run: 202
    # 2nd run: 422 ONKNOWN_FAILURE 'Error while creating packet'
    # Expected behaviour: According to Swagger documentation 'If no path is provided, a path which covers the nodes minimum required
    # hops will be determined automatically.' So, I expect this call should return 202, but better check with stakeholders
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = None),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [], hops = None),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    # 1st run: 400 INVALID_INPUT
    # 2nd run: 422 UNKNOWN_FAILURE Error while creating packet
    # Expected behaviour: Swagger documentation says about 'hops' param that 'This parameter is ignored if path is set'.
    # But if the parameter is set and 'path' is missing, I would expect that 'hops' param will be taken into consideration
    # and if its value is 0, which is forbidden, we should get some kind of 4xx error response.
    # The output is kind of good, in both cases we get a 4xx response, once 400 and once 422, but its a bit problematic since we
    # don't get consistently the same error code from the backend.
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = 0),
        # Output(expectedStatusCode = 422, expectedStatus = 'UNKNOWN_FAILURE', expectedErrorMessage = 'Error while creating packet')
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = None, hops = 1),
        # Output(expectedStatusCode = 422, expectedStatus = 'UNKNOWN_FAILURE', expectedErrorMessage = 'Error while creating packet')
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    # Here we have 400 error probably because if we have an empty path, 'hops' param will be taken into account if set,
    # and since 'hops' is 0, we have the 4xx error, because 'hops' must be between 1 and 3.
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [], hops = 0),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [], hops = 1),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    # 1st success run: 202
    # 2nd run: 422 UNKNOWN_FAILURE 'Error while creating packet.'
    # According to Swagger documentation, path and hops should be optional parameters, and 'hops' is
    # anyway ignored if a 'path' is given.
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [3], hops = None),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
        # Output(expectedStatusCode = 422, expectedStatus = 'UNKNOWN_FAILURE', expectedErrorMessage = 'Error while creating packet.')
    ),
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [3], hops = 0),
        Output(expectedStatusCode = 400, expectedStatus = 'INVALID_INPUT', expectedErrorMessage = None)
    ),
    # 1st run: 202
    # 2nd run: 422 UNKNOWN_FAILURE 'Error while creating packet.'
    (
        Input(sender = 1, receiver = 2, message = 'Hello from future', path = [3], hops = 1),
        Output(expectedStatusCode = 202, expectedStatus = None, expectedErrorMessage = None)
    ),
    # Notes:
    # - Cases with empty sender cannot be implemented, since the Python REST library will throw exceptions, because a valid URL
    # cannot be constructed without the index of the sender.
])
def test_case(input: Input, output: Output) -> None:
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
    
    response.close()

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
