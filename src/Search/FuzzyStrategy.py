from src.Search.SearchStrategy import SearchStrategy
from src.ExtractCV import ExtractCV
from src.Search.Fuzzy import Fuzzy

"""
Implementation of the SearchStrategy interface using the KMP algorithm.
"""
class FuzzyStrategy(SearchStrategy):

    def search(self, cv: ExtractCV, pattern: str) -> int:
        
        fuzzy_instance = Fuzzy(pattern, cv)
        results = fuzzy_instance.search()
        
        if (results):
            # print(f"Found {len(results)} matches for pattern '{pattern}' using Fuzzy Strategy.")
            return len(results)
        else:
            # print(f"No matches found for pattern '{pattern}' using Fuzzy Strategy.")
            return 0