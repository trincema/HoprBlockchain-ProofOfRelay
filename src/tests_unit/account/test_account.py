import pytest

from ...api_object_model.account.account import Account
from ...api_object_model.account.address import Address
from ...api_object_model.account.balance_type import BalanceType
from ...type.balance import Balance

@pytest.mark.parametrize("nodeIndex", [
    (1), (2), (3), (4), (5)
])
def test_balance(nodeIndex):
    """
    """
    account = Account()
    balanceData: Balance = account.get_balance(nodeIndex)
    assert balanceData.native >= 0
    assert balanceData.hopr >= 0

@pytest.mark.parametrize("nodeIndex", [
    (1), (2), (3), (4), (5)
])
def test_address(nodeIndex):
    """
    """
    account = Account()
    addressNative: str = account.get_address(nodeIndex, Address.NATIVE)
    assert addressNative.startswith("0x")

    addressHopr = account.get_address(nodeIndex, Address.HOPR)
    assert addressHopr.startswith("16U")

def test_withdraw():
    """
    """
    account = Account()
    receipt = account.withdraw(3, BalanceType.NATIVE, 10000, "0x59c833145D8adf4E2aB118307062dBde2d613CDF")
    print('Receipt: {}'.format(receipt))
    assert receipt.startswith('0x')