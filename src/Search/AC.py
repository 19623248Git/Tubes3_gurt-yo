from src.Search.ACTrie import ACTrie

'''
AC (Aho-Corasick) class for handling CV text extraction and manipulation.
This class searchs a word matching the string from ExtractCV class
'''
class AC:
        def __init__(self, pattern, cv):
                '''Initialize the AC class with a search string and an ExtractCV instance.'''
                self.cv = cv
                cv.extract()

                # initialize the AC Trie with the pattern
                self.ac_trie = ACTrie()
                self.ac_trie.insert(pattern)
                self.ac_trie.build_failure_links()

        def insert_pattern(self, pattern):
                '''Insert a new search pattern.'''
                self.ac_trie.insert(pattern)
                self.ac_trie.build_failure_links()

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
                res = []

                # Warning for empty text
                if n == 0:
                        print(f"Warning: Empty text provided")
                        return res

                # Warning for empty pattern
                if not self.ac_trie.root.children:
                        print("Warning: No patterns have been inserted into the trie.")
                        return res

                # Perform the Aho-Corasick search
                current_node = self.ac_trie.root

                for i,char in enumerate(text):
                        while current_node is not None and char not in current_node.children:
                                current_node = current_node.failure_link
                        
                        if current_node is None:
                                current_node = self.ac_trie.root
                                continue
                        
                        current_node = current_node.children[char]
                        
                        if current_node.output:
                                for pattern in current_node.output:
                                        res.append((i - len(pattern) + 1, pattern))

                return res
