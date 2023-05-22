import pytest
import timeit
import random
import string
from typing import List
import api_object_model.messages as messages
import api_object_model.node as node
import api_object_model.account as account
import api_object_model.messages as messages
import services.ws_api_service as wsApiService
import test_data.urls as urls

"""
Proposed Performance Tests
1. How much time would it take for message to arrive with a certain number of hops (1000 or 10.000 or 100.000)?
a. We can create a benchmark table to see a few timings and then decide on the number of hops we need to 'watch' for.
b. A discussion with business owner or clients would be usefull here, to determine whats important in terms of performance.
How are the clients actually plan to use the system? What are the business cases of the system?
c. What infrastructure/environment would we need setup for performance tests? With 5 nodes we can hardly have a close environment
to the production one. So, we have to define the test environment for performance testing.
2. 
"""

class Input:
    def __init__(self, sender: int, receiver: int, message: str, path: List[int], hops: int) -> None:
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.path = path
        self.hops = hops

class Output:
    def __init__(self, receivedMessage: str, visitationPath: List[List[int]]) -> None:
        self.receivedMessage = receivedMessage
        self.visitationPath = visitationPath

@pytest.mark.parametrize("input, output",[
    (
        Input(sender = 1, receiver = 2, message = "Hello from future", path = None, hops = 3),
        Output(receivedMessage = "", visitationPath = None)
    )
    ])
def test_performance_large_nb_hops(input: Input, output: Output):
    """
    It seems we can setup N-2 hops, where N is the maximum number of nodes in the network.
    So, in order to be able to implement this test for a large number of hops, we would need a special setup with
    the system having a couple thousands nodes, or how much nodes we would need for performance reasons.
    """
    # Instantiate needed objects
    nodeInstance = node.Node()
    accountInstance = account.Account()
    messagesInstance = messages.Messages()
    
    webSocket: wsApiService.WebsocketClientService = wsApiService.WebsocketClientService()
    webSocket.create_client_connection(input.receiver, urls.Urls.MESSAGES_SEND)
    print("senderNode = {}, testMessage = {}, recipient = {}, path = {}, hops = {}".format(
        input.sender, input.message, nodeInstance.get_peer_id(input.receiver), input.path, input.hops))
    
    start = timeit.timeit()
    messagesInstance.send_message(input.sender, input.message, nodeInstance.get_peer_id(input.receiver), input.path, input.hops)
    message2: str = webSocket.receive_message()
    assert output.receivedMessage in message2
    end = timeit.timeit()
    elapsed = end - start
    print("Elapsed: {}".format(elapsed))

@pytest.mark.parametrize("input, output",[
    (
        Input(sender = 1, receiver = 2, message = "", path = None, hops = 3),
        Output(receivedMessage = "", visitationPath = None)
    )
    ])
def test_performance_large_message_length(input: Input, output: Output):
    """
    Wanted to experiment with some performanc test on how much time it takes for the system to send a very large message,
    and observed that the websocket receives just 9 encoded numbers for the message: 200,128,134,1,136,31,181,74,52.
    TODO Have to investigate further here.
    """
    # Instantiate needed objects
    nodeInstance = node.Node()
    accountInstance = account.Account()
    messagesInstance = messages.Messages()

    largeMessage: str = random_char(10)
    largeMessage = 'Hello from future!'
    
    webSocket: wsApiService.WebsocketClientService = wsApiService.WebsocketClientService()
    webSocket.create_client_connection(input.receiver, urls.Urls.MESSAGES_SEND)
    print("senderNode = {}, testMessage = {}, recipient = {}, path = {}, hops = {}".format(
        input.sender, largeMessage, nodeInstance.get_peer_id(input.receiver), input.path, input.hops))
    
    start = timeit.timeit()
    messagesInstance.send_message(input.sender, input.message, nodeInstance.get_peer_id(input.receiver), input.path, input.hops)
    message2: str = webSocket.receive_message()
    end = timeit.timeit()
    print("Message: {}".format(message2))
    elapsed = end - start
    print("Elapsed: {}".format(elapsed))

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))