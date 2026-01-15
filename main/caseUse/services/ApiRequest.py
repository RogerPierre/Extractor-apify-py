
from main.models.interfaces.IInputUrl import IInputUrl

# Implementação da interface IInputUrl
class InputUrl(IInputUrl):
    def __init__(self, url: list[str]):
        self.url = url
    
    def get_url(self) -> list[str]:
        return self.url

