from src.Search.KMPStrategy import KMPStrategy
from src.Search.BMStrategy import BMStrategy
from src.Search.FuzzyStrategy import FuzzyStrategy

class Search:
        def __init__(self):
                self.strategies = {
                        'kmp': KMPStrategy(),
                        'bm': BMStrategy(),
                        'fuzzy': FuzzyStrategy(),  # Placeholder for future fuzzy search strategy
                }
                self.successStrategy = None
        
        def _search(self, strategy_name, text, pattern):
                """
                Perform a search using the specified strategy. If no matches are found with the specified strategy,
                it will fall back to the fuzzy search strategy.
                @param strategy_name: The name of the search strategy to use.
                @param text: The text to search within.
                @param pattern: The pattern to search for.
                @return: The number of matches found.
                """
                
                result = 0
                
                if strategy_name == 'kmp':
                        # print("Using KMP search strategy...")
                        result = self.strategies['kmp'].search(text, pattern)
                        if result > 0:
                                # print(f"Found {result} matches for pattern '{pattern}' using KMP Strategy.")
                                self.successStrategy = 'kmp'
                                return result
                elif strategy_name == 'bm':
                        # print("Using BM search strategy...")
                        result = self.strategies['bm'].search(text, pattern)
                        if result > 0:
                                # print(f"Found {result} matches for pattern '{pattern}' using BM Strategy.")
                                self.successStrategy = 'bm'
                                return result
                else:
                        print(f"Unknown search strategy: {strategy_name}")
                        return -1


                
                # if matches found, return the result
                if result != 0:
                        return result
                
                # print(f"No matches found for pattern '{pattern}' using Fuzzy Strategy.")
                

                result_fuzzy = self.strategies['fuzzy'].search(text, pattern) 
                if result_fuzzy != 0:
                        # print(f"Found {result_fuzzy} matches for pattern '{pattern}' using Fuzzy Strategy.")
                        self.successStrategy = 'fuzzy'
                        return result_fuzzy
                else:
                        # print(f"No matches found for pattern '{pattern}' using Any Strategy.")
                        self.successStrategy = None
                        return 0