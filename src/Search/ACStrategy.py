from src.Search.SearchStrategy import SearchStrategy
from src.Search.AC import AC
from src.ExtractCV import ExtractCV

"""
Implementation of the SearchStrategy interface using the AC algorithm.
"""
class ACStrategy(SearchStrategy):

        """
        Search for a pattern in the given CV using the Aho-Corasick algorithm.
        @param cv: The ExtractCV object containing the CV text.
        @param pattern: The PATTERNS to be searched, e.g. 'React, React Native, React Native Expo'.
        @return: The number of matches found.
        """
        def search(self, cv: ExtractCV, pattern: str) -> int:

                print("Using Aho-Corasick search algorithm...")

                patterns = [kw.strip().lower() for kw in pattern.split(',') if kw.strip()]

                ac_instance = AC(patterns[0], cv)

                for pattern in patterns[1:]:
                        ac_instance.insert_pattern(pattern)
                
                results = ac_instance.search()

                if(results):
                        print(f"Found {len(results)} matches for pattern '{pattern}' in the CV.")
                        return len(results)
                else:
                        print(f"No matches found for pattern '{pattern}' in the CV.")
                        return 0