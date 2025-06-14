import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.Search.Search import Search
from src.ExtractCV import ExtractCV

def test_search():
    # Initialize the Search class
    search_engine = Search()
    
    # Create a test CV with known content
    test_text = ExtractCV("../data/ACCOUNTANT/10554236.pdf")
    
    print("\n=== Testing KMP Search Strategy ===")
    # Test KMP with existing word
    result_kmp = search_engine._search('kmp', test_text, "accountant")
    print(f"KMP search result count: {result_kmp}")
    
    print("\n=== Testing BM Search Strategy ===")
    # Test BM with existing word
    result_bm = search_engine._search('bm', test_text, "accountant")
    print(f"BM search result count: {result_bm}")
    
    print("\n=== Testing Non-existent Word ===")
    # Test with a word that doesn't exist (should trigger fuzzy search)
    result_nonexistent = search_engine._search('kmp', test_text, "xyzabc123")
    print(f"Non-existent word search result count: {result_nonexistent}")
    
    print("\n=== Testing Invalid Strategy ===")
    # Test with invalid strategy
    result_invalid = search_engine._search('invalid_strategy', test_text, "test")
    print(f"Invalid strategy result: {result_invalid}")

def test_search_with_different_patterns():
    search_engine = Search()
    test_text = ExtractCV("../data/ACCOUNTANT/10554236.pdf")
    
    test_patterns = [
        "experience",    # Common word in CVs
        "skills",        # Another common word
        "education",     # Education section
        "2023",         # Year
        "management",    # Job-related term
        "",             # Empty string
        "a",            # Single character
        "the",          # Common word
        "zxcvbnm"       # Non-existent word
    ]
    
    print("\n=== Testing Different Patterns ===")
    for pattern in test_patterns:
        print(f"\nTesting pattern: '{pattern}'")
        # Test both KMP and BM for each pattern
        kmp_result = search_engine._search('kmp', test_text, pattern)
        bm_result = search_engine._search('bm', test_text, pattern)
        print(f"KMP found: {kmp_result} matches")
        print(f"BM found: {bm_result} matches")
        # Results should be the same for both algorithms
        assert kmp_result == bm_result, f"Inconsistent results for pattern '{pattern}': KMP={kmp_result}, BM={bm_result}"

if __name__ == "__main__":
    print("Starting Search tests...")
    test_search()
    print("\nTesting different patterns...")
    test_search_with_different_patterns()
    print("\nAll tests completed.")
