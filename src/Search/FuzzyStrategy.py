from SearchStrategy import SearchStrategy
from KMP import KMP

"""
Implementation of the SearchStrategy interface using the KMP algorithm.
"""
class FuzzyStrategy(SearchStrategy):

    def search(self, text: str, pattern: str) -> int:
        
        print("Using <insert Fuzzy Search Algorithm> search algorithm...")

        # logic for fuzzy search would go here