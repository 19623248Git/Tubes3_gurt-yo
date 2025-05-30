from ExtractCV import ExtractCV as ecv

'''
KMP (Knuth-Morris-Pratt) class for handling CV text extraction and manipulation.
This class searchs a word matching the string from ExtractCV class
'''
class KMP:
        def __init__(self, pattern, cv):
                '''Initialize the KMP class with a search string and an ExtractCV instance.'''
                self.cv = cv
                cv.extract()
                self.pattern = pattern
                self.lps = self.compute_lps(pattern)

        def set_pattern(self, pattern):
                '''Set a new search pattern.'''
                self.pattern = pattern
        
        def get_pattern(self):
                '''Get the current search pattern.'''
                return self.pattern

        def set_cv(self, cv):
                '''Set a new ExtractCV instance.'''
                self.cv = cv
        
        def get_cv(self):
                '''Get the current ExtractCV instance.'''
                return self.cv
        
        def compute_lps(self, pattern):
                '''Compute the longest prefix suffix (LPS) array for the KMP algorithm.'''
                lps = [0] * (len(pattern))
                length = 0  # Length of the previous longest prefix suffix
                i = 1
                
                # https://medium.com/@aakashjsr/preprocessing-algorithm-for-kmp-search-lps-array-algorithm-50e35b5bb3cb
                while(i < len(pattern)):
                        if(pattern[i] == pattern[length]):
                                length += 1
                                lps[i] = length
                                i += 1
                        else:
                                if(length != 0):
                                        length = lps[length - 1]
                                else:
                                        lps[i] = 0
                                        i += 1
                
                return lps
                        

        # https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
        def search(self):
                '''Search for the pattern in the CV text using KMP algorithm.'''
                text = self.cv.get_cleaned_text()
                n = len(text)
                m = len(self.pattern)
                res = []

                # Pointers i and j, for traversing 
                # the text and pattern
                i = 0
                j = 0

                while(i < n):

                        # If the characters match, move both pointers
                        if(self.pattern[j] == text[i]):
                                i += 1
                                j += 1

                                # If the entire pattern is found
                                if(j == m):
                                        res.append(i - j)

                                        # Reset j to the last matched prefix
                                        j = self.lps[j - 1]
                        
                        # if the characters do not match
                        else:
                                # If j is not 0, reset j to the last matched prefix
                                if(j != 0):
                                        j = self.lps[j - 1]
                                else:
                                        i += 1
                return res


