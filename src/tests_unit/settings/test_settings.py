import api_object_model.settings as settings

def test_case():
    """
    """
    settingsInstance = settings.Settings()
    sett = settingsInstance.get_settings(1)
    print(sett)