from abc import ABC, abstractmethod

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
        def search(self, text: str, pattern: str) -> int:
                pass