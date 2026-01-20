from main.Middler.ports.libs import ApifyService
from main.models.interfaces.IInputUrl import IInputUrl
from main.models.IRequests.IRequest import Requisition



# Implementação da interface Requisition para Apify


class Apify_request_tiktok(Requisition):
    def __init__(self, api_token: str, task_id: str, input_url: IInputUrl):
        self.client = ApifyService().create_A_Request(api_token)
        self.task_id = task_id
        self.input_url = input_url

    def fetch(self) -> list:
        try:
            request = {
              "commentsPerPost": 50,
              "excludePinnedPosts": False,
              "maxRepliesPerComment": 2,
              "postURLs": self.input_url.get_url(),
              "resultsPerPage": 100,
              "profileScrapeSections": [
                "videos"
              ],
              "profileSorting": "latest"
            }
            run = self.client.actor(self.task_id).call(run_input=request)
            items = self.client.dataset(run.get("defaultDatasetId"))
            outputs = []
            for item in items.iterate_items():
                outputs.append(item)
            return outputs
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                raise Exception(f"Ator não encontrado. Verifique se o task_id '{self.task_id}' está correto no Apify. Erro: {e}")
            else:
                raise Exception(f"Erro ao fazer a requisição: {e}")