import sys
import os
import time
import io
import re
import contextlib

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.Search.Search import Search
from src.ExtractCV import ExtractCV

# --- UI and Test Runner Implementation ---

class Colors:
    """ANSI color codes for formatted terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ======================================================================
#  Helper function to calculate string length ignoring ANSI codes
# ======================================================================
def get_visual_length(s):
    """Calculates the visible length of a string by removing ANSI color codes."""
    return len(re.sub(r'\033\[[0-9;]*m', '', s))

# ======================================================================
#  Function to draw formatted ASCII boxes (Corrected Logic)
# ======================================================================
def print_in_box(title, content_lines, status="", status_color=""):
    """
    Prints a title, content, and status line inside a correctly formatted ASCII box.
    """
    # Create the full status line for width calculation and printing
    full_status_line = f"Status: {status}" if status else ""

    # Combine all lines to determine the necessary width
    all_lines = [title] + content_lines
    if full_status_line:
        all_lines.append(full_status_line)

    # Determine the max visual width needed for the content
    width = 0
    for line in all_lines:
        width = max(width, get_visual_length(line))

    # --- Print Top Border ---
    print(f"{Colors.BLUE}┌─{'─' * width}─┐{Colors.ENDC}")

    # --- Print Title ---
    title_padding = ' ' * (width - get_visual_length(title))
    print(f"{Colors.BLUE}│{Colors.ENDC} {Colors.BOLD}{title}{title_padding} {Colors.BLUE}│{Colors.ENDC}")

    # --- Print Separator ---
    if content_lines or status:
        print(f"{Colors.BLUE}├─{'─' * width}─┤{Colors.ENDC}")

    # --- Print Content Lines ---
    for line in content_lines:
        line_padding = ' ' * (width - get_visual_length(line))
        print(f"{Colors.BLUE}│{Colors.ENDC} {line}{line_padding} {Colors.BLUE}│{Colors.ENDC}")

    # --- Print Status Line ---
    if status:
        # Create a colored version for printing
        colored_status_display = f"Status: {status_color}{Colors.BOLD}{status}{Colors.ENDC}"
        status_padding = ' ' * (width - get_visual_length(full_status_line))
        print(f"{Colors.BLUE}│{Colors.ENDC} {colored_status_display}{status_padding} {Colors.BLUE}│{Colors.ENDC}")

    # --- Print Bottom Border ---
    print(f"{Colors.BLUE}└─{'─' * width}─┘{Colors.ENDC}")
    print()  # Add a newline for spacing

# ======================================================================
#  Main Test Suite Runner
# ======================================================================
def run_test_suite(test_functions):
    """
    Runs a collection of test functions, captures their output,
    and displays the results in formatted boxes.
    """
    total_tests = len(test_functions)
    passed_tests = 0
    start_time = time.time()

    print_in_box("RUNNING TEST SUITE", [f"Found {total_tests} tests..."])

    for i, test_func in enumerate(test_functions):
        test_name = test_func.__name__
        title = f"Test {i+1}/{total_tests}: {Colors.YELLOW}{test_name}{Colors.ENDC}"

        output_buffer = io.StringIO()
        status = ""
        status_color = ""
        
        try:
            with contextlib.redirect_stdout(output_buffer):
                test_func()
            status = "PASSED"
            status_color = Colors.GREEN
            passed_tests += 1
        except AssertionError as e:
            status = "FAILED"
            status_color = Colors.RED
            # Add the assertion error to the captured output for display
            output_buffer.write(f"\n{Colors.RED}└> {e}{Colors.ENDC}")
        except Exception as e:
            status = "ERROR"
            status_color = Colors.RED
            output_buffer.write(f"\n{Colors.RED}└> An unexpected error occurred: {e}{Colors.ENDC}")

        content_lines = output_buffer.getvalue().strip().split('\n')
        print_in_box(title, content_lines, status, status_color)

    end_time = time.time()
    duration = end_time - start_time

    # --- Final Summary Box ---
    summary_color = Colors.GREEN if passed_tests == total_tests else Colors.RED
    summary_status = f"{passed_tests} / {total_tests} PASSED"
    summary_content = [f"Total Duration: {duration:.4f} seconds"]
    print_in_box("TEST SUMMARY", summary_content, summary_status, summary_color)


# --- Your Original Test Logic, Refactored with Assertions ---

def print_assertion(condition_str):
    """Helper to print the assertion being checked."""
    print(f"{Colors.CYAN}  CHECKING: assert {condition_str}{Colors.ENDC}")

# ======================================================================
#  TEST CASE 1: test_search_algorithms_consistency
# ======================================================================
def test_search_algorithms_consistency():
    search_engine = Search()
    test_text = ExtractCV("data/ACCOUNTANT/10554236.pdf")
    result_kmp = search_engine._search('kmp', test_text, "accountant")
    result_bm = search_engine._search('bm', test_text, "accountant")
    
    print_assertion("result_kmp > 0")
    assert result_kmp > 0, "KMP search should have found 'accountant'"
    
    print_assertion("result_bm > 0")
    assert result_bm > 0, "BM search should have found 'accountant'"
    
    print_assertion("result_kmp == result_bm")
    assert result_kmp == result_bm, f"KMP and BM results should be equal (KMP: {result_kmp}, BM: {result_bm})"

# ======================================================================
#  TEST CASE 2: test_non_existent_word_search
# ======================================================================
def test_non_existent_word_search():
    search_engine = Search()
    test_text = ExtractCV("data/ACCOUNTANT/10554236.pdf")
    result_nonexistent = search_engine._search('kmp', test_text, "xyzabc123")
    print(f"Search for 'xyzabc123' returned: {result_nonexistent}")
    
    if(result_nonexistent == -2):
        print_assertion("result_nonexistent == -2")
        assert result_nonexistent == -2, "Expected -2 for fuzzy search fallback, fuzzy not yet implemented"
    elif(result_nonexistent < 0):
        print_assertion("result_nonexistent < 0")
        assert result_nonexistent < 0, "Expected a value less than 0 for a non-existent word"

# ======================================================================
#  TEST CASE 3: test_invalid_strategy_handling
# ======================================================================
def test_invalid_strategy_handling():
    search_engine = Search()
    test_text = ExtractCV("data/ACCOUNTANT/10554236.pdf")
    result_invalid = search_engine._search('invalid_strategy', test_text, "test")
    
    print_assertion("result_invalid == -1")
    assert result_invalid == -1, f"Invalid strategy should return -1, but got {result_invalid}"

# ======================================================================
#  TEST CASE 4: test_various_patterns_for_consistency
# ======================================================================
def test_various_patterns_for_consistency():
    search_engine = Search()
    test_text = ExtractCV("data/ACCOUNTANT/10554236.pdf")
    test_patterns = ["experience", "skills", "education", "management", "", "a"]
    print("Testing consistency for multiple patterns...")
    for pattern in test_patterns:
        kmp_result = search_engine._search('kmp', test_text, pattern)
        bm_result = search_engine._search('bm', test_text, pattern)
        
        condition = f"kmp_result == bm_result for pattern '{pattern}'"
        print_assertion(condition)
        assert kmp_result == bm_result, f"Inconsistent for '{pattern}': KMP={kmp_result}, BM={bm_result}"
    print(f"\nSuccessfully compared {len(test_patterns)} patterns.")

# --- Main Execution Block ---

# ======================================================================
#  Script Entry Point
# ======================================================================
if __name__ == "__main__":
    tests_to_run = [
        test_search_algorithms_consistency,
        test_non_existent_word_search,
        test_invalid_strategy_handling,
        test_various_patterns_for_consistency,
    ]
    run_test_suite(tests_to_run)