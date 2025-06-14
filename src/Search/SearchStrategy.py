from abc import ABC, abstractmethod
from src.ExtractCV import ExtractCV

"""
The Strategy interface for supported search algorithms.
"""
class SearchStrategy(ABC):
        
        """
        Search for a pattern in the given text.
        @param text: The text to search within.
        @param pattern: The pattern to search for.
        @return: The number of matches found.
        """
        @abstractmethod
        def search(self, cv: ExtractCV, pattern: str) -> int:
                pass