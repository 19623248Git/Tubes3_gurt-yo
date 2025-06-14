NO_OF_CHARS = 256

'''
BM (Boyer-Moore) class for handling CV text extraction and manipulation.
This class searches for a word matching the string from ExtractCV class
using the Boyer-Moore algorithm.
'''
class BM:
        def __init__(self, pattern, cv):
                '''
                Initialize the BM class with a search pattern and an ExtractCV instance.
                '''
                self.cv = cv
                self.cv.extract()
                self.pattern = pattern
                self.bad_char = self.bad_char_heuristic(pattern)

        def set_pattern(self, pattern):
                '''
                Set a new search pattern.
                '''
                self.pattern = pattern
                self.bad_char = self.bad_char_heuristic(pattern)

        def get_pattern(self):
                '''Get the current search pattern.'''
                return self.pattern

        def set_cv(self, cv):
                '''Set a new ExtractCV instance.'''
                self.cv = cv

        def get_cv(self):
                '''Get the current ExtractCV instance.'''
                return self.cv

        # https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/
        def bad_char_heuristic(self, pattern):
                '''
                Compute the bad character heuristic table for the Boyer-Moore algorithm.
                '''
                m = len(pattern)
                # Initialize all occurrences as -1
                bad_char = [-1] * NO_OF_CHARS

                # Fill the actual value of the last occurrence of a character
                for i in range(m):
                        bad_char[ord(pattern[i])] = i
                return bad_char

        def search(self):
                '''
                Search for the pattern in the CV text using the Boyer-Moore algorithm
                with the Bad Character Heuristic.
                '''
                text = ""
                text = self.cv.get_cleaned_text()

                n = len(text)
                m = len(self.pattern)
                res = []

                # Warning for empty pattern or text
                if m == 0:
                        print(f"Warning: Empty pattern provided")
                        return res
                if n == 0:
                        print(f"Warning: Empty text provided")
                        return res

                s = 0  # shift
                while s <= n - m:
                        j = m - 1
                        while j >= 0 and self.pattern[j] == text[s + j]:
                                j -= 1
                        if j < 0:
                                res.append(s)

                                if s + m < n:
                                        char_after_match_val = self.bad_char[ord(text[s + m])]
                                        shift_val = m - char_after_match_val
                                        s += shift_val
                                else:
                                        s += 1
                        else:
                                # Mismatch at pattern[j] and text[s+j]. Shift pattern
                                bad_char_in_text_val = self.bad_char[ord(text[s + j])]
                                shift = j - bad_char_in_text_val
                                s += max(1, shift)
                return res