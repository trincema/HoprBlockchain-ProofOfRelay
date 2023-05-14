import pytest
import time
from typing import List
import api_object_model.node as node
import api_object_model.account as account
import api_object_model.messages as messages
import services.ws_api_service as wsApiService
import test_data.urls as urls

class Input:
    sender: int
    receiver: int
    message: str
    path = []
    hops: int

class Output:
    receivedMessage: str
    visitationPath = []


@pytest.mark.parametrize("input, output",[
    ({1, 2, "Hello from future", [3], 0},
     {"217,145,72,101,108,108,111,32,102,114,111,109,32,102,117", [1, 3, 2]})
    ])
def test_case1(input: Input, output: Output):
    """
    :sender: The index of the sender node (like '1' for node1)
    :receiver: The index of the receiver node (like '2' for node2)
    :message: The message to send from 'sender' to 'receiver'
    :path: Array of node indexes through which the message should be routed from sender to receiver
    :hops: The number of hops through which the message should be randomly routed
    :receivedMessage: Expected received message by 'receiver', encoded as Uint8Array of numbers
    :visitationPath: Array of node indexes representing the path the message should take from 'sender' to 'receiver'
    """
    # Instantiate needed objects
    nodeInstance = node.Node()
    accountInstance = account.Account()
    messagesInstance = messages.Messages()
    
    # Step1: Send the test message from senderNode to receiverNode
    webSocket: wsApiService.WebsocketClientService = wsApiService.WebsocketClientService()
    webSocket.create_client_connection(input.receiver, urls.Urls.MESSAGES_SEND)
    peerIdPath = []
    for nodeId in input.path:
        peerIdPath.append(nodeInstance.get_peer_id(nodeId))
    print("senderNode = {}, testMessage = {}, recipient = {}, path = {}, hops = {}".format(
        input.sender, input.message, nodeInstance.get_peer_id(input.receiver), peerIdPath, input.hops))
    messagesInstance.send_message(input.sender, input.message, nodeInstance.get_peer_id(input.receiver), peerIdPath, input.hops)

    # Step2: Check that the message is received by receiverNode
    message2: str = webSocket.receive_message()
    assert output.receivedMessage in message2

    # Step3: Check the visitation path
    currentEpochTime = int(time.time())
    for pair in output.visitationPath:
        lastSeenPair = nodeInstance.get_announced_last_seen(pair[0], nodeInstance.get_peer_id(pair[1]))
        lastSeenPairDelta = (currentEpochTime - lastSeenPair/1000)
        print("lastSeenPair = {}, epochTime = {}, lastSeenPairDelta = {}".format(lastSeenPair, currentEpochTime, lastSeenPairDelta))
        assert lastSeenPairDelta < 60     # Check that it was last visited in the last minute
    # Or another alternative here would be to check the last seen diference before calling the /message API
    # TODO have to make some improvements to this check

    # Step4: Check that the message is not received by other nodes
    for otherReceiverNode in range(1, 6):
        if otherReceiverNode != input.receiver:
            messagesInstance.check_node_does_not_get_message(input.receiver, urls.Urls.MESSAGES_SEND)

    # Step5: ?Check that the balance is/not charged by the message?
    # TODO use accountInstance here

    webSocket.close_client_connection()

def xtest_case3():
    """
    Test case 3: Test send message from Node1 to Node2 with one defined hop and a random hop
    Note: the random hop has to be ignored in this case
    """
    # Define test data for this scenario
    senderNode = 1
    receiverNode = 2
    testMessage = "Hello from future"
    expectedEncodedMessage = "217,145,72,101,108,108,111,32,102,114,111,109,32,102,117"
    visitationPath = [[1, 3], [3, 2]]
    path = [3]
    hops = 1

def xtest_case4():
    """
    Test case 4: Test send message from Node1 to Node2 with one random hop and no defined hop
    TODO - Here the tricky part is to extend the template to check which node from the other 3 nodes is visited
    """
    pass
