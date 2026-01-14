from apify_client import ApifyClient
from ...models.interfaces.services import ApiServiceInterface
class ApifyService(ApiServiceInterface):
    def create_A_Request(self, api_token: str) -> ApifyClient:
        return ApifyClient(api_token)