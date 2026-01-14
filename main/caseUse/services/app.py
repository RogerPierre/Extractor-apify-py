import os
import csv
from datetime import datetime
from main.Middler.ports.libs import ApifyService
from main.models.interfaces.IInputUrl import IInputUrl
from main.models.IRequests.IRequest import Requisition
from main.models.IRequests.OutputComents import OutputComents

# Implementação da interface IInputUrl
class InputUrl(IInputUrl):
    def __init__(self, url: str):
        self.url = url
    
    def get_url(self) -> str:
        return self.url

# Implementação da interface Requisition para Apify
class ApifyRequest(Requisition):
    def __init__(self, api_token: str, task_id: str, input_url: IInputUrl):
        self.client = ApifyService().create_A_Request(api_token)
        self.task_id = task_id
        self.input_url = input_url
    
    def fetch(self) -> dict:
        try:
            request = {
                "url": self.input_url.get_url(),
                # Adicione outros parâmetros conforme necessário para extrair comentários
            }
            response = self.client.actor(self.task_id).call(run_input=request)
            return response
        except Exception as e:
            raise Exception(f"Erro ao fazer a requisição: {e}")

# Implementação da interface OutputComents
class CommentsParser(OutputComents):
    def parse_comments(self, data: dict) -> list:
        # Assumindo que os dados retornados têm uma chave 'comments' com lista de comentários
        comments = data.get('comments', [])
        return comments

# Função principal para extrair comentários
def extract_comments(api_token: str, task_id: str, url: str) -> list:
    input_url = InputUrl(url)
    request = ApifyRequest(api_token, task_id, input_url)
    data = request.fetch()
    parser = CommentsParser()
    comments = parser.parse_comments(data)
    return comments

# Exemplo de uso
if __name__ == "__main__":
    api_token = 'YOUR_API_TOKEN'
    task_id = 'YOUR_TASK_ID'  # ID do task do Apify para extrair comentários
    url = "https://example.com"  # Substitua pela URL desejada
    comments = extract_comments(api_token, task_id, url)
    print(comments)
