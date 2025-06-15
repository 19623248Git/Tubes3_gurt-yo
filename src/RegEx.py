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

def extract_section_text(text, target_section_keywords, all_stop_headings):
    """
    Extracts text for a target section, stopping at the next known heading.
    """
    _, start_pos = find_section(text, target_section_keywords)
    if start_pos == -1:
        return "Not Found"

    end_pos = len(text)
    
    # Find the start of the *next* section to determine the end of the current one
    # We search the text *after* the start of our current section
    text_after_start = text[start_pos + 1:] 
    
    for heading in all_stop_headings:
        # We don't want to match the keywords of the section we are currently in
        if heading.lower() in [kw.lower() for kw in target_section_keywords]:
            continue

        _, next_section_pos = find_section(text_after_start, [heading])
        if next_section_pos != -1:
            # Position is relative, so add it back to get absolute position
            absolute_pos = start_pos + 1 + next_section_pos
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
    target_sections = {
        'summary': ['professional summary', 'executive profile', 'career overview', 'executive summary','summary', 'overview', 'profile', 'objective'],
        'skills': [ 'areas of expertise', 'skill highlights', 'core strengths', 'core qualifications','skills', 'abilities', 'technologies'],
        'experience': ['professional experience', 'work experience', 'teaching experience','experience', 'work history', 'employment history'],
        'education': [ 'education and training','education', 'qualifications']
    }

    all_known_headings = [ # Universal Map
        # Summary
        'Executive Profile','career overview', 'executive summary', 'Summary', 'Overview', 'Profile', 'Objective', 
        # Skills
        'Areas of Expertise','Skill Highlights', 'core strengths', 'core qualifications','Skills', 'Abilities', 'Technologies', 
        # Experience
         'Work experience', 'Teaching experience','Professional Experience', 'Experience','Work History', 'Employment History', 
        # Education
        'Education and Training','Education', 
        # Stop words
        'Accomplishments', 'Highlights', 'Additional Information', 'References', 'Website and Links', 'Affiliations'
    ]

    extracted_data = {}
    for section_name, keywords in target_sections.items():
        extracted_data[section_name] = extract_section_text(text, keywords, all_known_headings)

    return extracted_data