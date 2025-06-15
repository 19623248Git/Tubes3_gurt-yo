import re

def find_section_by_pattern(text, patterns):
    """
    Find the start of a section based on regex patterns.
    Returns the matched text and its start position.
    """
    for pattern in patterns:
        try:
            # Match patterns at the beginning of a line, allowing for whitespace
            full_pattern = r'^\s*' + pattern + r'\s*$'
            match = re.search(full_pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group().strip(), match.start()
        except re.error:
            continue
    return None, -1

def extract_section_by_pattern(text, target_patterns, all_stop_patterns):
    """
    Extracts text for a target section using regex patterns, stopping at the next known heading.
    """
    matched_header, start_pos = find_section_by_pattern(text, target_patterns)
    if start_pos == -1:
        return "Not Found"

    end_pos = len(text)
    
    # Find the start of the *next* section to determine the end of the current one
    text_after_start = text[start_pos + 1:] 
    
    for stop_pattern in all_stop_patterns:
        # Skip patterns that might match our current section
        if any(re.search(target_pat, matched_header, re.IGNORECASE) for target_pat in target_patterns):
            # Check if the stop pattern would match our current header
            if re.search(stop_pattern, matched_header, re.IGNORECASE):
                continue

        _, next_section_pos = find_section_by_pattern(text_after_start, [stop_pattern])
        if next_section_pos != -1:
            # Position is relative, so add it back to get absolute position
            absolute_pos = start_pos + 1 + next_section_pos
            end_pos = min(end_pos, absolute_pos)

    # Extract the text from after the header line to the start of the next section
    section_header_match = re.search(r'.*', text[start_pos:])
    if section_header_match:
        start_after_header = start_pos + section_header_match.end()
        return text[start_after_header:end_pos].strip()
    
    return "Not Found"

def extract_all_details(text):
    """
    Extracts all required sections using regex patterns for more flexible matching.
    """
    # Define regex patterns for each section type
    section_patterns = {
        'summary': [
            r'(?:professional\s+)?summary',
            r'executive\s+(?:profile|summary)',
            r'career\s+overview',
            r'(?:professional\s+)?overview',
            r'(?:professional\s+)?profile',
            r'(?:career\s+)?objective',
            r'personal\s+statement'
        ],
        'skills': [
            r'core\s+qualifications\b',
            r'(?:technical\s+)?skills?\b',
            r'(?:core\s+)?(?:competencies|qualifications)\b',
            r'areas?\s+of\s+expertise\b',
            r'skill\s+highlights?\b',
            r'core\s+strengths?\b',
            r'(?:technical\s+)?abilities\b',
            r'technologies\b',
            r'key\s+skills?\b',
            r'technical\s+(?:skills?|competencies)\b'
        ],
        'experience': [
            r'(?:professional\s+|work\s+)?experience',
            r'(?:work|employment)\s+history',
            r'career\s+history',
            r'professional\s+background',
            r'work\s+experience',
            r'teaching\s+experience',
            r'relevant\s+experience'
        ],
        'education': [
            r'education(?:\s+(?:and|&)\s+(?:training|qualifications))?',
            r'(?:academic\s+)?qualifications?',
            r'educational\s+background',
            r'academic\s+credentials',
            r'degrees?'
        ]
    }

    # All possible section patterns for stopping points
    all_stop_patterns = [
        # Summary variations
        r'(?:professional\s+)?summary',
        r'executive\s+(?:profile|summary)',
        r'career\s+overview',
        r'(?:professional\s+)?overview',
        r'(?:professional\s+)?profile',
        r'(?:career\s+)?objective',
        r'personal\s+statement',
        
        # Skills variations
        r'core\s+qualifications\b',
        r'(?:technical\s+)?skills?\b',
        r'(?:core\s+)?(?:competencies|qualifications)\b',
        r'areas?\s+of\s+expertise\b',
        r'skill\s+highlights?\b',
        r'core\s+strengths?\b',
        r'(?:technical\s+)?abilities\b',
        r'technologies\b',
        r'key\s+skills?\b',
        r'technical\s+(?:skills?|competencies)\b',
        
        # Experience variations
        r'(?:professional\s+|work\s+)?experience',
        r'(?:work|employment)\s+history',
        r'career\s+history',
        r'professional\s+background',
        r'work\s+experience',
        r'teaching\s+experience',
        r'relevant\s+experience',
        
        # Education variations
        r'education(?:\s+(?:and|&)\s+(?:training|qualifications))?',
        r'(?:academic\s+)?qualifications?',
        r'educational\s+background',
        r'academic\s+credentials',
        r'degrees?',
        
        # Common stopping sections
        r'accomplishments?',
        r'(?:key\s+)?achievements?',
        r'highlights?',
        r'additional\s+information',
        r'references?',
        r'(?:website|web)\s+(?:and\s+)?links?',
        r'affiliations?',
        r'certifications?',
        r'awards?',
        r'publications?',
        r'projects?',
        r'volunteer\s+(?:work|experience)',
        r'languages?',
        r'interests?',
        r'hobbies'
    ]

    extracted_data = {}
    for section_name, patterns in section_patterns.items():
        extracted_data[section_name] = extract_section_by_pattern(text, patterns, all_stop_patterns)

    return extracted_data

# Additional utility functions for more advanced pattern matching
def find_all_sections(text):
    """
    Find all sections in the document with their positions.
    Useful for debugging or getting an overview of document structure.
    """
    # Common section header pattern
    section_pattern = r'^\s*([A-Z][A-Za-z\s&]+)\s*$'
    sections = []
    
    for match in re.finditer(section_pattern, text, re.MULTILINE):
        sections.append({
            'title': match.group(1).strip(),
            'position': match.start(),
            'line_number': text[:match.start()].count('\n') + 1
        })
    
    return sections

def extract_custom_section(text, custom_pattern, all_stop_patterns=None):
    """
    Extract a section using a custom regex pattern.
    """
    if all_stop_patterns is None:
        # Use default stop patterns if none provided
        all_stop_patterns = [
            r'(?:professional\s+)?summary', r'(?:technical\s+)?skills?', 
            r'(?:professional\s+)?experience', r'education', r'references?'
        ]
    
    return extract_section_by_pattern(text, [custom_pattern], all_stop_patterns)