'''
Fuzzy string matching class as a fallback for exact matching strategies.
'''

class Fuzzy:
    def __init__(self, pattern, cv):
        '''Initialize the Fuzzy class with a search string and an ExtractCV instance.'''
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
    
    def levenshtein_distance(self, s1, s2):
        '''Calculate the Levenshtein distance between two strings.'''
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
    
    def calculate_threshold_from_length(self, length):
        '''Calculate a threshold based on the length of the pattern.'''
        if length < 5:
            return 1
        elif length < 10:
            return 2
        elif length < 20:
            return 3
        else:
            return 4

    def search(self):
        '''Search for the pattern in the CV text using fuzzy matching.'''
        text = self.cv.get_cleaned_text()
        
        # print(f"Performing fuzzy search for '{self.pattern}' in CV text.")
        MIN_THRESHOLD = 1
        MAX_THRESHOLD = self.calculate_threshold_from_length(len(self.pattern))        
        words = text.split()
        matches = []
        for word in words:
            distance = self.levenshtein_distance(self.pattern, word)
            if distance >= MIN_THRESHOLD and distance <= MAX_THRESHOLD:
                matches.append(word)
        if matches:
            # print(f"Found {len(matches)} matches for pattern '{self.pattern}' using Fuzzy Strategy.")
            return matches
        else:
            # print(f"No matches found for pattern '{self.pattern}' using Fuzzy Strategy.")
            return []