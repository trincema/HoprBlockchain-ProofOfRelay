from typing import List
import api_object_model.tickets as tickets
import api_object_model.node as node
import type.ticket as ticket

def test_case1():
    """
    """
    nodeInstance = node.Node()
    ticketsInstance = tickets.Tickets()

    nodeInstance.get_node_info(1)
    nodeInstance.get_node_info(2)
    nodeInstance.get_node_info(3)
    nodeInstance.get_node_info(4)
    nodeInstance.get_node_info(5)

    # ticketsList = List[ticket.Ticket] = ticketsInstance.get_all_tickets(3)