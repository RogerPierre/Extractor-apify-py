from abc import ABC, abstractmethod

class ApiServiceInterface(ABC):

    @abstractmethod
    def create_A_Request(self, api_token: str) -> object:
        pass