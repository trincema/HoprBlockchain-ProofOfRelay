import pytest
import time
from typing import List
import api_object_model.node as node
import api_object_model.account as account
import api_object_model.messages as messages
import api_object_model.tickets as tickets
import type.ticket as ticket
import type.ticket_statistics as ticketStatistics
import type.balance as balance
import services.ws_api_service as wsApiService
import test_data.urls as urls

TICKET_RELAY_VALUE = 10000000000000000

class Input:
    def __init__(self, sender: int, receiver: int, message: str, path: List[int], hops: int) -> None:
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.path = path
        self.hops = hops

class Output:
    def __init__(self, receivedMessage: str, visitationPath: List[List[int]], relayNode: int) -> None:
        self.receivedMessage = receivedMessage
        self.visitationPath = visitationPath
        self.relayNode = relayNode

@pytest.mark.parametrize("input, output",[
    (
        Input(sender = 1, receiver = 2, message = "Hello from future", path = [3], hops = None),
        Output(receivedMessage = "217,145,72,101,108,108,111,32,102,114,111,109,32,102,117", visitationPath = [[1, 3], [3, 2]], relayNode = 3)
    )
    ])
def test_case1(input: Input, output: Output):
    """
    Send message cost: 0.01HOPR
    :sender: The index of the sender node (like '1' for node1)
    :receiver: The index of the receiver node (like '2' for node2)
    :message: The message to send from 'sender' to 'receiver'
    :path: Array of node indexes through which the message should be routed from sender to receiver
    :hops: The number of hops through which the message should be randomly routed
    :receivedMessage: Expected received message by 'receiver', encoded as Uint8Array of numbers
    :visitationPath: Array of node indexes representing the path the message should take from 'sender' to 'receiver'
    """
    # Instantiate needed objects and prepare data
    nodeInstance = node.Node()
    nodeIndexes = list(range(1, 6))
    ticketsStatistics: List[ticketStatistics.TicketStatistics] = get_tickets_statistics(nodeIndexes)
    balances: List[balance.Balance] = get_balances(nodeIndexes)
    peerIdPath = []
    for nodeId in input.path:
        peerIdPath.append(nodeInstance.get_peer_id(nodeId))
    wsConnections: List[wsApiService.WebsocketClientService] = get_websocket_connections([1, 3, 4, 5], urls.Urls.MESSAGES_SEND, 5)
    
    check_send_message(input, output, peerIdPath)
    check_message_not_received([1, 3, 4, 5], wsConnections, input)
    # check_visitation_path(input, output)
    check_proof_of_relay(nodeIndexes, ticketsStatistics, output.relayNode)
    check_redeeming_tickets(nodeIndexes, balances, output.relayNode)    

def check_send_message(input: Input, output: Output, peerIdPath: List[int]):
    """
    Send the test message from senderNode to receiverNode.
    Check that the message is received by receiver node.
    """
    messagesInstance = messages.Messages()
    nodeInstance = node.Node()
    webSocket: wsApiService.WebsocketClientService = wsApiService.WebsocketClientService(input.receiver, urls.Urls.MESSAGES_SEND)
    
    messagesInstance.send_message(input.sender, input.message, nodeInstance.get_peer_id(input.receiver), peerIdPath, input.hops)
    message2: str = webSocket.receive_message()
    assert output.receivedMessage in message2
    webSocket.close_client_connection()

def check_message_not_received(nodeIndexes: List[int], wsConnections: List[wsApiService.WebsocketClientService], input: Input):
    """
    Check that the sent message was not received by other nodes other than the receiver node.
    """
    messagesInstance = messages.Messages()
    for index in range(len(nodeIndexes)):
        nodeIndex = nodeIndexes[index]
        wsConnection = wsConnections[index]
        messagesInstance.check_node_does_not_get_message(nodeIndex, wsConnection)

def check_visitation_path(input: Input, output: Output):
    """
    Check that the relay nodes have been visited.
    """
    nodeInstance = node.Node()
    currentEpochTime: int = int(time.time())
    for pair in output.visitationPath:
        lastSeenPair = nodeInstance.get_announced_last_seen(pair[0], nodeInstance.get_peer_id(pair[1]))
        lastSeenPairDelta: int = currentEpochTime - int(lastSeenPair/1000)
        print("lastSeenPair = {}, epochTime = {}, lastSeenPairDelta = {}".format(lastSeenPair, currentEpochTime, lastSeenPairDelta))
        assert lastSeenPairDelta < 60     # Check that it was last visited in the last minute
    # Or another alternative here would be to check the last seen diference before calling the /message API
    # TODO have to make some improvements to this check

def check_proof_of_relay(nodeIndexes: List[int], previousTicketsStatistics: List[ticketStatistics.TicketStatistics], nodeIndex: int) -> None:
    """
    Check that the proof of relay mechanism was properly followed: the tickets are received (node properly incentivized) by a node after
    a message has been relayed.
    :previousTicketsStatistics: Previous (before message relay) ticket statistics data to check agaist
    :nodeIndex: The node index to be checked for PoR (tickets received)
    """
    ticketsStatistics: List[ticketStatistics.TicketStatistics] = get_tickets_statistics(nodeIndexes)
    # Check that the tickets status data is correctly updated
    previous: ticketStatistics.TicketStatistics = previousTicketsStatistics[nodeIndex - 1]
    current: ticketStatistics.TicketStatistics = ticketsStatistics[nodeIndex - 1]

    assert current.pending - previous.pending == 0
    assert current.unredeemed - previous.unredeemed == 1
    assert current.unredeemedValue - previous.unredeemedValue == TICKET_RELAY_VALUE
    assert current.redeemed - previous.redeemed == 0
    assert int(current.redeemedValue) - int(previous.redeemedValue) == 0

def check_redeeming_tickets(nodeIndexes: List[int], previousBalances: List[balance.Balance], nodeIndex: int):
    """
    Checking the tickets redeeming of given node.
    :previousBalances:
    :return:
    """
    # Check that the balance is charged by the send message operation
    # On playground the cost of transfer is 0, so can't test this functionality
    currentBalances = get_balances(nodeIndexes)
    previousTicketsStatistics: List[ticketStatistics.TicketStatistics] = get_tickets_statistics(nodeIndexes)

    previous: balance.Balance = previousBalances[nodeIndex - 1]
    current: balance.Balance = currentBalances[nodeIndex - 1]

    assert current.native - previous.native == 0
    assert current.hopr - previous.hopr == 0

    ticketsInstance = tickets.Tickets()
    ticketsInstance.redeem_all_tickets(nodeIndex)

    ticketsStatistics: List[ticketStatistics.TicketStatistics] = get_tickets_statistics(nodeIndexes)
    current: ticketStatistics.TicketStatistics = ticketsStatistics[nodeIndex - 1]
    previous: ticketStatistics.TicketStatistics = previousTicketsStatistics[nodeIndex - 1]
    assert current.redeemed - previous.redeemed == 1
    assert int(current.redeemedValue) - int(previous.redeemedValue) == TICKET_RELAY_VALUE
    assert previous.unredeemed - current.unredeemed == 1
    assert previous.unredeemedValue - current.unredeemedValue == TICKET_RELAY_VALUE

    # TODO Check NATIVE and HOPR balances after redeem operation
    #currentBalances = get_balances(nodeIndexes)
    #current: balance.Balance = currentBalances[nodeIndex - 1]
    #assert int(previous.native) - int(current.native) == 133705500000000
    #assert current.hopr - previous.hopr == 0

def tickets_still_pending(ticketsStatistics: List[ticketStatistics.TicketStatistics]) -> None:
    """
    """
    stillPending = False
    for ticketsStatistic in ticketsStatistics:
        if ticketsStatistic.pending > 0:
            stillPending = True
    return stillPending

def get_tickets_statistics(nodeIndexes: List[int]) -> List[ticketStatistics.TicketStatistics]:
    """
    Getting the ticket statistics for all the nodes in the test environment (works for small number of test nodes)
    :nodeIndexes: The list of node indexes for which to get the balances.
    :return: A list of 'TicketStatistics' objects, with the corresponding given nodes statistics.
    """
    ticketsInstance = tickets.Tickets()
    ticketsStatistics: List[ticketStatistics.TicketStatistics] = []
    for nodeIndex in nodeIndexes:
        ticketsStatistics.append(ticketsInstance.get_tickets_statistics(nodeIndex))
    return ticketsStatistics

def get_balances(nodeIndexes: List[int]):
    """
    Get current (when this function is called) blances for the given list of nodes.
    :nodeIndexes: The list of node indexes for which to get the balances.
    :return: A list of 'Balance' objects, with the corresponding given nodes balances.
    """
    accountInstance = account.Account()
    balanceList: List[balance.Balance] = []
    for nodeIndex in nodeIndexes:
        balanceList.append(accountInstance.get_balance(nodeIndex))
    return balanceList

def get_websocket_connections(nodeIndexes: List[int], path: str, timeout: int = 30) -> List[wsApiService.WebsocketClientService]:
    """
    """
    wsConnections: List[wsApiService.WebsocketClientService] = []
    for nodeIndex in nodeIndexes:
        wsConnections.append(wsApiService.WebsocketClientService(nodeIndex, path, timeout))
    return wsConnections