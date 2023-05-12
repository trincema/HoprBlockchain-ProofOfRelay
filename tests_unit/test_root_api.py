import api_object_model.root_api as rootApi

def test_base_url():
    root = rootApi.RootApi()
    base = root.get_base_hostname()
    assert base == "localhost"