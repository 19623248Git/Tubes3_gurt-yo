from src.Search.SearchStrategy import SearchStrategy
from src.Search.AC import AC
from src.ExtractCV import ExtractCV
from typing import Dict, List

"""
Implementation of the SearchStrategy interface using the AC algorithm.
"""
class ACStrategy(SearchStrategy):
        """
        Search for patterns in the given CV using the Aho-Corasick algorithm.
        This strategy fulfills the interface contract by returning the total number
        of matches found (int).
        
        It also stores the detailed results (a dictionary of pattern occurrences)
        in the `last_results` property for richer data extraction.
        """
        def __init__(self):
                """Initializes the strategy and the property for storing detailed results."""
                self.last_results: Dict[str, List[int]] = {}

        def search(self, cv: ExtractCV, pattern: str) -> int:
                """
                Searches for a comma-separated string of patterns.

                @param cv: The ExtractCV object containing the CV text.
                @param pattern: A comma-separated string of patterns to search for (e.g., 'React, Java').
                @return: The total number of occurrences found, as an integer.
                """
                print("Using Aho-Corasick search algorithm...")

                patterns = [kw.strip().lower() for kw in pattern.split(',') if kw.strip()]

                if not patterns:
                        self.last_results = {}
                        print("Warning: No patterns provided to search for.")
                        return 0

                ac_instance = AC(patterns[0], cv)
                for p in patterns[1:]:
                        ac_instance.insert_pattern(p)
                
                details = ac_instance.search()

                self.last_results = details

                if not details:
                        print(f"No matches found for the specified patterns in the CV.")
                        return 0

                total_occurrences = sum(len(indices) for indices in details.values())

                print(f"Found a total of {total_occurrences} occurrences for {len(details)} unique pattern(s).")

                return total_occurrences