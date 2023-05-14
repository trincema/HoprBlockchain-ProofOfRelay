import api_object_model.node as node
import api_object_model.account as account
import api_object_model.messages as messages
import services.ws_api_service as wsApiService
import test_data.urls as urls
import time

class MessagesTemplates:
    """
    Define common templates for testing the messages and feed it with data
    """
    
    def __init__(self) -> None:
        pass

    def template1(self, senderNode: int, receiverNode: int,
                  testMessage: str, expectedEncodedMessage: str,
                  visitationPath = [[]],
                  path = [], hops: int = 0) -> None:
        """
        Step1: Send a message from senderNode to receiverNode
        Step2: Check that the message is received by receiver node
        Step3: 
        """
        # Instantiate needed objects
        nodeInstance = node.Node()
        accountInstance = account.Account()
        messagesInstance = messages.Messages()
        
        # Step1: Send the test message from senderNode to receiverNode
        webSocket: wsApiService.WebsocketClientService = wsApiService.WebsocketClientService()
        webSocket.create_client_connection(receiverNode, urls.Urls.MESSAGES_SEND)
        peerIdPath = []
        for nodeId in path:
            peerIdPath.append(nodeInstance.get_peer_id(nodeId))
        print("senderNode = {}, testMessage = {}, recipient = {}, path = {}, hops = {}".format(
            senderNode, testMessage, nodeInstance.get_peer_id(receiverNode), peerIdPath, hops))
        messagesInstance.send_message(senderNode, testMessage, nodeInstance.get_peer_id(receiverNode), peerIdPath, hops)

        # Step2: Check that the message is received by receiverNode
        message2: str = webSocket.receive_message()
        assert expectedEncodedMessage in message2

        # Step3: Check the visitation path
        currentEpochTime = int(time.time())
        for pair in visitationPath:
            lastSeenPair = nodeInstance.get_announced_last_seen(pair[0], nodeInstance.get_peer_id(pair[1]))
            lastSeenPairDelta = (currentEpochTime - lastSeenPair/1000)
            print("lastSeenPair = {}, epochTime = {}, lastSeenPairDelta = {}".format(lastSeenPair, currentEpochTime, lastSeenPairDelta))
            assert lastSeenPairDelta < 60     # Check that it was last visited in the last minute
        # Or another alternative here would be to check the last seen diference before calling the /message API
        # TODO have to make some improvements to this check

        # Step4: Check that the message is not received by other nodes
        for otherReceiverNode in range(1, 6):
            if otherReceiverNode != receiverNode:
                messagesInstance.check_node_does_not_get_message(receiverNode, urls.Urls.MESSAGES_SEND)

        # Step5: ?Check that the balance is/not charged by the message?
        # TODO use accountInstance here

        webSocket.close_client_connection()