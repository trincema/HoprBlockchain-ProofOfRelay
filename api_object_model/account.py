
from enum import Enum
from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
import type.balance as balance

class BalanceType(Enum):
    NATIVE = 0,
    HOPR = 1

class Address(Enum):
    NATIVE = 0,
    HOPR = 1

class Account(RootApi):
    """
    Account object wrapper with all useful methods to interact with a certain node addresses, balances, and withdrawals.
    """
    
    def __init__(self) -> None:
        super().__init__()

    def withdraw(self, nodeIndex: int, balanceType: BalanceType, amount: int, recipient: str) -> str:
        """
        Withdraw funds from this node to your ethereum wallet address. You can choose whitch currency you want to withdraw, NATIVE or HOPR.
        :recipient: ETH address where the funds will be sent to
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.ACCOUNT_WITHDRAW)
        payload = {
            "currency": balanceType.name,
            "amount": str(amount),
            "recipient": recipient
        }
        print('url = {}, payload = {}'.format(url, payload))
        restService = restApiService.RestApiService(self.get_auth_token())
        response: Response = restService.post_request(url, payload)
        if response.status_code == 200:
            # Withdraw successful. Receipt from this response can be used to check details of the transaction on ethereum network.
            return response.json()['receipt']
        else:
            self.handle_http_error(response)
    
    def get_balance(self, nodeIndex: int) -> balance.Balance:
        """
        Get node's HOPR and NATIVE balances.
        HOPR tokens from this balance is used to fund payment channels between this node and other nodes on the network.
        NATIVE balance is used to pay for the gas fees for the blockchain network.
        :nodeIndex:
        :return:
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.ACCOUNT_BALANCES)
        return balance.Balance(
            int(data[BalanceType.NATIVE.name.lower()]),
            int(data[BalanceType.HOPR.name.lower()]))
    
    def get_balances(self, nodeIndex):
        """
        :nodeIndex: The index of the node for which the balances need to be fetched
        :return: A Balances object with both NATIVE and HOPR balances for a certain node index
        """
        balanceNative = self.get_balance(nodeIndex, BalanceType.NATIVE)


    def get_address(self, nodeIndex, address: Address) -> str:
        """
        Get node's HOPR and native addresses. HOPR address is also called PeerId and can be used by other node owner to interact with this node.
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.ACCOUNT_ADDRESSES)
        return data[address.name.lower()]

    def other_utility_method_around_these_APIs(self) -> None:
        """
        """
        pass