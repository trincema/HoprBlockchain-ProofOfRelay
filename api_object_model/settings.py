from .root_api import RootApi
import test_data.urls as urls
import services.rest_api_service as restApiService
from requests import Response
from enum import Enum
from strenum import StrEnum

class Setting(StrEnum):
    AUTO_REDEEM_TICKETS = 'autoRedeemTickets',
    INCLUDE_RECIPIENT = 'includeRecipient',
    STRATEGY = 'strategy'

class StrategySetting(Enum):
    PASSIVE = 0,
    PROMISCUOUS = 1

class Settings(RootApi):
    def __init__(self) -> None:
        super().__init__()
    
    def get_settings(self, nodeIndex) -> str:
        """
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.SETTINGS_GET_NODE_SETTINGS)
        return data
    
    def set_setting(self, nodeIndex: int, setting: Setting, value: str) -> bool:
        """
        Change this node's setting value. Check Settings schema to learn more about each setting and the type of value it expects.
        """
        url = self.get_rest_url(nodeIndex, urls.Urls.SETTINGS_UPDATE_NODE_SETTING_VALUE)
        restService = restApiService.RestApiService(self.get_auth_token())
        response: Response = restService.put_request(url)
        if response.status_code != 204:
            # Setting set succesfully
            return True
        else:
            self.handle_http_error(response)
        return False
    
    def is_auto_redemption_tickets(self, nodeIndex: int) -> bool:
        """
        Check if auto redemption setting is set on a specific node.
        :nodeIndex: The index of the node to which the setting should be applied
        """
        restService = restApiService.RestApiService(self.get_auth_token())
        data = restService.get_request(nodeIndex, urls.Urls.SETTINGS_GET_NODE_SETTINGS)
        return bool(data[Setting.AUTO_REDEEM_TICKETS.lower()])
    
    def set_auto_redemption_tickets(self, nodeIndex: int, value: bool) -> bool:
        """
        :nodeIndex: The index of the node to which the setting should be applied
        :value: True or False
        """
        return self.set_setting(nodeIndex, Setting.AUTO_REDEEM_TICKETS.value, value)

    def is_include_recipient(self, nodeIndex: int, value: bool) -> bool:
        """
        """
        
    
    def set_include_recipient(self, nodeIndex: int, value: bool) -> bool:
        """
        :nodeIndex: The index of the node to which the setting should be applied
        :value: True or False
        """
        return self.set_setting(nodeIndex, Setting.INCLUDE_RECIPIENT.value, value)