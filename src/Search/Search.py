from src.Search.KMPStrategy import KMPStrategy
from src.Search.BMStrategy import BMStrategy
from src.Search.FuzzyStrategy import FuzzyStrategy
from src.Search.ACStrategy import ACStrategy

class Search:
        def __init__(self):
                self.strategies = {
                        'kmp': KMPStrategy(),
                        'bm': BMStrategy(),
                        'ac': ACStrategy(),
                        'fuzzy': FuzzyStrategy(),
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
                        result = self.strategies['kmp'].search(text, pattern)
                        if result > 0:
                                self.successStrategy = 'kmp'
                elif strategy_name == 'bm':
                        result = self.strategies['bm'].search(text, pattern)
                        if result > 0:
                                self.successStrategy = 'bm'
                elif strategy_name == 'ac':
                        result = self.strategies['ac'].search(text, pattern)
                        if result > 0:
                                self.successStrategy = 'ac'
                elif strategy_name == 'fuzzy':
                        result = self.strategies['fuzzy'].search(text, pattern)
                        if result > 0:
                                self.successStrategy = 'fuzzy'
                else:
                        print(f"Unknown search strategy: {strategy_name}")
                        return -1
                
                return result