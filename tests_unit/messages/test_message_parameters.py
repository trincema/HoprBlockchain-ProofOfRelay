import pytest
import json
from typing import List
import api_object_model.node as node
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import api_object_model.channels as channels
import api_object_model.root_api as rootApi


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
    )
])

def xtest_case():
    """
    The 2nd type of Test Case we can have is to test the boundary values of the message.
    Case 1: Send an empty message
    Case 2: Send 1 character message
    Case 3: Send special character message
    Case 4: Which is the maximum length of message supported by the platform? HTTP supports from 1MB to 1GB
    as the maximum size of the payload, so we can explore with larger messages to see what happens.
    """
    pass