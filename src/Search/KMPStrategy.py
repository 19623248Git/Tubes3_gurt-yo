from SearchStrategy import SearchStrategy
from KMP import KMP

"""
Implementation of the SearchStrategy interface using the KMP algorithm.
"""
class KMPStrategy(SearchStrategy):

    def search(self, text: str, pattern: str) -> int:
        
        print("Using KMP search algorithm...")

        kmp_instance = KMP(pattern, text)
        results = kmp_instance.search()

        if(results):
                print(f"Found {len(results)} matches for pattern '{pattern}' in the text.")
                return len(results)
        else:
                print(f"No matches found for pattern '{pattern}' in the text.")
                return 0