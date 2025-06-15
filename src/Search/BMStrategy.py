from src.Search.SearchStrategy import SearchStrategy
from src.Search.BM import BM
from src.ExtractCV import ExtractCV

"""
Implementation of the SearchStrategy interface using the BM algorithm.
"""
class BMStrategy(SearchStrategy):

    def search(self, cv: ExtractCV, pattern: str) -> int:

        print("Using BM search algorithm...")

        bm_instance = BM(pattern, cv)
        results = bm_instance.search()

        if(results):
                print(f"Found {len(results)} matches for pattern '{pattern}' in the CV.")
                return len(results)
        else:
                print(f"No matches found for pattern '{pattern}' in the CV.")
                return 0