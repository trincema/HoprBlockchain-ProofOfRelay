
from enum import Enum
from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService

class Currency(Enum):
    NATIVE = 'NATIVE',
    HOPR = 'HOPR'

class Account(RootApi):
    """
    Account object wrapper with all useful methods to interact with a certain node addresses, balances, and withdrawals.
    """
    
    def __init__(self) -> None:
        super().__init__()

    def withdraw(self, currency: Currency, amount: int, recipient: str) -> None:
        """
        Withdraw funds from this node to your ethereum wallet address. You can choose whitch currency you want to withdraw, NATIVE or HOPR.
        """
        pass

    def get_node_balance(self, nodeIndex: int, currency: Currency) -> int:
        """
        Get node's HOPR and native balances. HOPR tokens from this balance is used to fund payment channels between this node and other
        nodes on the network. NATIVE balance is used to pay for the gas fees for the blockchain network.
        """
        url = 'http://{baseUrl}:{port}/{serverUrl}/{balances}'.format(
            baseUrl = self.get_base_hostname(),
            port = self.get_port(nodeIndex),
            serverUrl = self.get_server_url(),
            balances = urls.Urls.ACCOUNT_BALANCES
        )
        restService = restApiService.RestApiService(self.get_auth_token())
        response = restService.get_request(url)

        if response.status_code == 200:
            if currency == Currency.NATIVE:
                nativeBalance = response.json()["native"]
                return int(nativeBalance)
            elif currency == Currency.HOPR:
                hoprBalance = response.json()["hopr"]
                return int(hoprBalance)
        else:
            # Handle errors according to the Swagger API specs
            self.handle_http_error(response)

    def get_address(self) -> None:
        """
        Get node's HOPR and native addresses. HOPR address is also called PeerId and can be used by other node owner to interact with this node.
        """
        pass

    def other_utility_method_around_these_APIs(self) -> None:
        """
        """
        pass