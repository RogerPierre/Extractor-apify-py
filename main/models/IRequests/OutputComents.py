from abc import ABC, abstractmethod 

class OutputComents(ABC):
    @abstractmethod
    def parse_comments(self, data: dict) -> list:
        """Parse comments from the given data."""
        pass