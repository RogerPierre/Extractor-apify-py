import os
import csv
from main.Middler.ports.libs import ApifyService   
from main.models.interfaces.IInputUrl import IInputUrl
from main.models.IRequests.IRequest import Requisition
from main.models.IRequests.OutputComents import OutputComents
from main.caseUse.services.ApiRequest import InputUrl
# Implementação da interface Requisition para Apify


class ApifyRequest(Requisition):
    def __init__(self, api_token: str, task_id: str, input_url: IInputUrl):
        self.client = ApifyService().create_A_Request(api_token)
        self.task_id = task_id
        self.input_url = input_url
    
    def fetch(self) -> dict:
        try:
            request = {
                
            "directUrls": self.input_url.get_url(),
            "resultsLimit": 150,
            "isNewestComments": True,
                # Adicione outros parâmetros conforme necessário para extrair comentários
            }
            print(f"[DEBUG] Tentando executar ator com task_id: {self.task_id}")
            print(f"[DEBUG] URL sendo enviada: {self.input_url.get_url()}")
            response = self.client.actor(self.task_id).call(run_input=request)
            return response
        except Exception as e:
            error_msg = str(e)
            print(f"[ERRO] Task ID usado: {self.task_id}")
            print(f"[ERRO] Detalhes: {error_msg}")
            if "not found" in error_msg.lower():
                raise Exception(f"Ator não encontrado. Verifique se o task_id '{self.task_id}' está correto no Apify. Erro: {e}")
            else:
                raise Exception(f"Erro ao fazer a requisição: {e}")

# Implementação da interface OutputComents
class CommentsParser(OutputComents):
    def parse_comments(self, data: dict) -> list:
        # Assumindo que os dados retornados têm uma chave 'comments' com lista de comentários
        comments = data.get('comments', [])
        return comments

# Função principal para extrair comentários
def extract_comments(api_token: str, task_id: str, url: list[str]) -> list:
    input_url = InputUrl(url)
    request = ApifyRequest(api_token, task_id, input_url)
    data = request.fetch()
    parser = CommentsParser()
    comments = parser.parse_comments(data)
    return comments

