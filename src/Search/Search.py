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
        
        def _search(self, strategy_name, text, pattern):
                """
                Perform a search using the specified strategy.
                @param strategy_name: The name of the search strategy to use.
                @param text: The text to search within.
                @param pattern: The pattern to search for.
                @return: The number of matches found.
                """
                
                if strategy_name  == 'fuzzy':
                        print("Fuzzy search strategy can not be called directly.")
                elif strategy_name == 'kmp':
                        print("Using KMP search strategy...")
                        result = self.strategies['kmp'].search(text, pattern)
                        if result > 0:
                                print(f"Found {result} matches for pattern '{pattern}' using KMP Strategy.")
                                return result
                elif strategy_name == 'bm':
                        print("Using BM search strategy...")
                        result = self.strategies['bm'].search(text, pattern)
                        if result > 0:
                                print(f"Found {result} matches for pattern '{pattern}' using BM Strategy.")
                                return result
                else:
                        print(f"Unknown search strategy: {strategy_name}")
                        return -1

                # if no matches found, try fuzzy search first
                print(f"No matches found for pattern '{pattern}' using Fuzzy Strategy.")
                
                # Temporary return statement to avoid errors
                # if implemented remove this line
                return -2
        

                result_fuzzy = self.strategies['fuzzy'].search(text, pattern) 
                if result_fuzzy > 0:
                        print(f"Found {result_fuzzy} matches for pattern '{pattern}' using Fuzzy Strategy.")
                        return result_fuzzy
                else:
                        print(f"No matches found for pattern '{pattern}' using Any Strategy.")
                        return 0