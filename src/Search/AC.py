'''
AC (Aho-Corasick) class for handling CV text extraction and manipulation.
This class searchs a word matching the string from ExtractCV class
'''
class AC:
        def __init__(self, pattern, cv):
                '''Initialize the AC class with a search string and an ExtractCV instance.'''
                self.cv = cv
                cv.extract()
                self.pattern = pattern

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
        
        def search(self):
                '''Search for the pattern in the CV text using AC algorithm.'''
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

                


