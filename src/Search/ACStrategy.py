from src.Search.SearchStrategy import SearchStrategy
from src.Search.AC import AC
from src.ExtractCV import ExtractCV

"""
Implementation of the SearchStrategy interface using the AC algorithm.
"""
class ACStrategy(SearchStrategy):

    def search(self, cv: ExtractCV, pattern: str) -> int:

        print("Using Aho-Corasick search algorithm...")

        ac_instance = AC(pattern, cv)
        results = ac_instance.search()

        if(results):
                print(f"Found {len(results)} matches for pattern '{pattern}' in the CV.")
                return len(results)
        else:
                print(f"No matches found for pattern '{pattern}' in the CV.")
                return 0