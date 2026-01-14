from abc import ABC, abstractmethod

class IInputUrl(ABC):
    @abstractmethod
    def get_url(self) -> str:
        """Retrieve the input URL."""
        pass
    