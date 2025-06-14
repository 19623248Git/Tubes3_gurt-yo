from src.Search.SearchStrategy import SearchStrategy
from src.Search.BM import BM

"""
Implementation of the SearchStrategy interface using the BM algorithm.
"""
class BMStrategy(SearchStrategy):

    def search(self, text: str, pattern: str) -> int:

        print("Using BM search algorithm...")

        bm_instance = BM(pattern, text)
        results = bm_instance.search()

        if(results):
                print(f"Found {len(results)} matches for pattern '{pattern}' in the text.")
                return len(results)
        else:
                print(f"No matches found for pattern '{pattern}' in the text.")
                return 0