import re

def find_section(text, keywords):
    """
    Find the start of a section based on a list of keywords.
    Returns the keyword and its start position.
    """
    for keyword in keywords:
        try:
            pattern = r'^\s*' + re.escape(keyword) + r'\s*$'
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                return keyword, match.start()
        except re.error:
            continue
    return None, -1

def extract_section_text(text, start_keyword, all_sections):
    """
    Extracts text from a section, starting from the start_keyword
    and ending at the beginning of the next section.
    """
    # Find the start position of the current section's keyword
    _, start_pos = find_section(text, [start_keyword])
    if start_pos == -1:
        return "Not Found"

    # Find the end position (the start of the next closest section)
    end_pos = len(text)
    
    # Find start of all other sections to determine where current section ends
    for section_name, section_keywords in all_sections.items():
        if section_name != start_keyword:
            # Find other keywords that appear *after* the current section starts
            _, next_section_pos = find_section(text[start_pos:], section_keywords)
            if next_section_pos != -1:
                # Position is relative to the start_pos, so add it back
                absolute_pos = start_pos + next_section_pos
                if absolute_pos > start_pos:
                    end_pos = min(end_pos, absolute_pos)

    # Extract the text from after the keyword's line to the start of the next section
    section_header_match = re.search(r'.*', text[start_pos:])
    if section_header_match:
        start_after_header = start_pos + section_header_match.end()
        return text[start_after_header:end_pos].strip()
    
    return "Not Found"

def extract_all_details(text):
    """
    Extracts all required sections (Summary, Skills, Experience, Education) from the CV text.
    """
    section_definitions = {
        'summary': ['summary', 'overview', 'profile', 'objective', 'professional summary'],
        'skills': ['skills', 'abilities', 'technologies'],
        'experience': ['experience', 'work history', 'employment history', 'professional experience'],
        'education': ['education', 'qualifications', 'education and training']
    }

    extracted_data = {}
    for section_name in section_definitions:
        extracted_data[section_name] = extract_section_text(text, section_name, section_definitions)

    return extracted_data