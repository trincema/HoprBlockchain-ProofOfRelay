import api_object_model.account as account

def test_balance_native():
    acc = account.Account()
    balance: int = acc.get_node_balance(1, account.Currency.NATIVE)
    assert balance >= 0

def test_balance_hopr():
    acc = account.Account()
    balance: int = acc.get_node_balance(1, account.Currency.HOPR)
    assert balance >= 0