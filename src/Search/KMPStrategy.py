from src.Search.SearchStrategy import SearchStrategy
from src.Search.KMP import KMP
from src.ExtractCV import ExtractCV

"""
Implementation of the SearchStrategy interface using the KMP algorithm.
"""
class KMPStrategy(SearchStrategy):

    def search(self, cv: ExtractCV, pattern: str) -> int:
        
        # print("Using KMP search algorithm...")

        kmp_instance = KMP(pattern, cv)
        results = kmp_instance.search()

        if(results):
                # print(f"Found {len(results)} matches for pattern '{pattern}' in the CV.")
                return len(results)
        else:
                # print(f"No matches found for pattern '{pattern}' in the CV.")
                return 0