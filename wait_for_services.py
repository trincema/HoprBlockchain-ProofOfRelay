import api_object_model.root_api as rootApi
import test_data.urls as urls
import services.rest_api_service as restService
from requests import Response
import time

rootAtiInstance = rootApi.RootApi()
authToken = rootAtiInstance.get_auth_token()
for nodeIndex in range(1, 6):
    url = 'http://localhost:1330{}/api/v2/{}'.format(nodeIndex, urls.Urls.NODE_INFO)
    restService = restService.RestApiService(authToken)
    while True:
        response: Response = restService.get_request(url)
        if response.status_code == 200:
            break
        else:
            time.sleep(5)