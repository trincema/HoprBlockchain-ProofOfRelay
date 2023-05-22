from typing import List
from .root_api import RootApi
import test_data.urls as urls
import type.ticket as ticket
import type.ticket_statistics as ticketStatistics
import services.rest_api_service as restApiService
import json

class Tickets(RootApi):
    """
    Tickets API object wrapper with all useful methods to interact with tickets in the HOPR network.
    """

    def __init__(self) -> None:
        super().__init__()
        self.restService = restApiService.RestApiService(self.get_auth_token())
    
    def get_all_tickets(self, nodeIndex: int) -> List[ticket.Ticket]:
        """
        Get all tickets earned from every channel by a node by relaying data packets.
        :nodeIndex: The node for which to fetch all the tickets.
        :return: List of Ticket objects with all the tickets.
        """
        data = self.restService.get_request(nodeIndex, urls.Urls.TICKETS_LIST)
        tickets: List[ticket.Ticket] = []
        print('data = {}'.format(json.dumps(data)))
        for dataTicket in data:
            # TODO Find a better, generic and shorter way to map this, json.loads() doesn't seem to help much since
            # we also have arrays returned from some of the API calls
            tickets.append(ticket.Ticket(
                dataTicket[ticket.TicketKey.COUNTERPARTY.value],
                dataTicket[ticket.TicketKey.CHALLENGE.value],
                dataTicket[ticket.TicketKey.EPOCH.value],
                dataTicket[ticket.TicketKey.INDEX.value],
                dataTicket[ticket.TicketKey.AMOUNT.value],
                dataTicket[ticket.TicketKey.WIN_PROB.value],
                dataTicket[ticket.TicketKey.CHANNEL_EPOCH.value],
                dataTicket[ticket.TicketKey.SIGNATURE.value]))
        return tickets
    
    def redeem_all_tickets(self, nodeIndex: int) -> None:
        """
        Redeems all tickets from all the channels and exchanges them for Hopr tokens.
        Every ticket have a chance to be winning one, rewarding you with Hopr tokens.
        :nodeIndex:
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.TICKETS_REDEEM)
        payload = {}
        response = self.restService.post_request(url, payload)
        if response.status_code >=  400:
            self.handle_http_error(response)
    
    def get_tickets_statistics(self, nodeIndex: int, ticketsStatisticsKey: ticketStatistics.TicketStatisticsKey) -> int:
        """
        Get statistics regarding all your tickets. Node gets a ticket everytime it relays data packet in channel.
        Get a certain statistic value for the given node index.
        :nodeIndex: The node number for which the specific statistics is to be fetched.
        :ticketsStatisticsKey: The type of ticket statistics we want to fetch for the given node.
        :return: The desired statistic value as a number.
        """
        return int(self._get_tickets_statistics(nodeIndex, ticketsStatisticsKey.value))

    def get_tickets_statistics(self, nodeIndex: int) -> object:
        """
        """
        data = self.restService.get_request(nodeIndex, urls.Urls.TICKETS_STATISTICS)
        print('data = {}'.format(json.dumps(data)))
        # TODO Find a better, generic and shorter way to map this, json.loads() doesn't seem to help much since
        # we also have arrays returned from some of the API calls, or have numbers defined as strings (redeemed/unredeemedValue),
        # so more granular interfacing is needed (at least for these more complicated types)
        ticketsStatistics = ticketStatistics.TicketStatistics(
            data[ticketStatistics.TicketStatisticsKey.PENDING.value],
            data[ticketStatistics.TicketStatisticsKey.UNREDEEMED.value],
            int(data[ticketStatistics.TicketStatisticsKey.UNREDEEMED_VALUE.value]),
            int(data[ticketStatistics.TicketStatisticsKey.REDEEMED.value]),
            data[ticketStatistics.TicketStatisticsKey.REDEEMED_VALUE.value],
            data[ticketStatistics.TicketStatisticsKey.LOSING_TICKETS.value],
            data[ticketStatistics.TicketStatisticsKey.WIN_PROPORTION.value],
            data[ticketStatistics.TicketStatisticsKey.NEGLECTED.value],
            data[ticketStatistics.TicketStatisticsKey.REJECTED.value],
            data[ticketStatistics.TicketStatisticsKey.REJECTED_VALUE.value])
        return ticketsStatistics
    
    def _get_tickets_statistics(self, nodeIndex: int, statisticKey: str) -> str:
        """
        """
        data = self.restService.get_request(nodeIndex, urls.Urls.TICKETS_STATISTICS)
        return int(data[statisticKey])