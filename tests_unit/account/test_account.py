import pytest
import api_object_model.account as account
import type.balance as balance

@pytest.mark.parametrize("nodeIndex", [
    (1), (2), (3), (4), (5)
])
def test_balance(nodeIndex):
    """
    """
    acc = account.Account()
    balanceData: balance.Balance = acc.get_balance(nodeIndex)
    assert balanceData.native >= 0
    assert balanceData.hopr >= 0

@pytest.mark.parametrize("nodeIndex", [
    (1), (2), (3), (4), (5)
])
def test_address(nodeIndex):
    """
    """
    acc = account.Account()
    addressNative: str = acc.get_address(nodeIndex, account.Address.NATIVE)
    assert addressNative.startswith("0x")

    addressHopr = acc.get_address(nodeIndex, account.Address.HOPR)
    assert addressHopr.startswith("16U")

def test_withdraw():
    """
    """
    acc = account.Account()
    receipt = acc.withdraw(3, account.BalanceType.NATIVE, 10000, "0x59c833145D8adf4E2aB118307062dBde2d613CDF")
    print('Receipt: {}'.format(receipt))
    assert receipt.startswith('0x')