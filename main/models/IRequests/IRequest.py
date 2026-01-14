from abc import ABC, abstractmethod

class Requisition(ABC):
    @abstractmethod
    def fetch(self) -> dict:
        """Fetch data from the request."""
        pass