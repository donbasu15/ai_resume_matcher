import spacy
import re
from fuzzywuzzy import fuzz, process
from .skills_database import get_all_skills, get_skills_by_category, get_skill_synonyms

# Load pre-trained spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install spaCy English model: python -m spacy download en_core_web_sm")
    nlp = None

def extract_skills(text: str, skill_list: list = None, threshold: int = 80) -> dict:
    """Enhanced skill extraction with fuzzy matching and categorization."""
    if skill_list is None:
        skill_list = get_all_skills()
    
    text_lower = text.lower()
    found_skills = {
        'exact_matches': [],
        'fuzzy_matches': [],
        'by_category': {}
    }
    
    # Get skill synonyms
    synonyms = get_skill_synonyms()
    
    # Exact matching
    for skill in skill_list:
        skill_lower = skill.lower()
        if skill_lower in text_lower:
            found_skills['exact_matches'].append(skill)
    
    # Fuzzy matching for skills not found exactly
    remaining_skills = [s for s in skill_list if s not in found_skills['exact_matches']]
    
    # Extract potential skill phrases from text
    doc = nlp(text) if nlp else None
    potential_skills = []
    
    if doc:
        # Extract noun phrases and entities
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Focus on shorter phrases
                potential_skills.append(chunk.text.lower())
        
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                potential_skills.append(ent.text.lower())
    
    # Add individual words
    words = re.findall(r'\b\w+\b', text_lower)
    potential_skills.extend(words)
    
    # Remove duplicates
    potential_skills = list(set(potential_skills))
    
    # Fuzzy matching
    for potential_skill in potential_skills:
        if len(potential_skill) > 2:  # Skip very short words
            match = process.extractOne(potential_skill, remaining_skills, scorer=fuzz.ratio)
            if match and match[1] >= threshold:
                found_skills['fuzzy_matches'].append(match[0])
    
    # Check synonyms
    for skill, syns in synonyms.items():
        if skill not in found_skills['exact_matches'] and skill not in found_skills['fuzzy_matches']:
            for syn in syns:
                if syn.lower() in text_lower:
                    found_skills['exact_matches'].append(skill)
                    break
    
    # Categorize skills
    all_found = list(set(found_skills['exact_matches'] + found_skills['fuzzy_matches']))
    skills_by_cat = get_skills_by_category()
    
    for category, cat_skills in skills_by_cat.items():
        found_in_category = [skill for skill in all_found if skill in cat_skills]
        if found_in_category:
            found_skills['by_category'][category] = found_in_category
    
    return found_skills

def extract_experience_level(text: str) -> dict:
    """Extract years of experience and level indicators."""
    text_lower = text.lower()
    
    # Extract years of experience
    years_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
        r'experience.*?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s*in',
        r'over\s*(\d+)\s*years?',
        r'more\s*than\s*(\d+)\s*years?'
    ]
    
    years_found = []
    for pattern in years_patterns:
        matches = re.findall(pattern, text_lower)
        years_found.extend([int(match) for match in matches])
    
    # Determine experience level
    level_keywords = {
        'entry': ['entry level', 'junior', 'graduate', 'fresher', 'trainee', 'intern'],
        'mid': ['mid level', 'intermediate', 'experienced', 'specialist'],
        'senior': ['senior', 'lead', 'principal', 'staff', 'expert'],
        'executive': ['director', 'manager', 'head', 'chief', 'vp', 'vice president', 'ceo', 'cto', 'cfo']
    }
    
    detected_levels = []
    for level, keywords in level_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_levels.append(level)
                break
    
    max_years = max(years_found) if years_found else 0
    avg_years = sum(years_found) / len(years_found) if years_found else 0
    
    return {
        'years_mentioned': years_found,
        'max_years': max_years,
        'average_years': round(avg_years, 1),
        'levels_detected': list(set(detected_levels)),
        'inferred_level': infer_level_from_years(max_years)
    }

def infer_level_from_years(years: int) -> str:
    """Infer experience level from years of experience."""
    if years == 0:
        return 'entry'
    elif years <= 2:
        return 'entry'
    elif years <= 5:
        return 'mid'
    elif years <= 10:
        return 'senior'
    else:
        return 'executive'

def extract_education(text: str) -> dict:
    """Extract education information."""
    text_lower = text.lower()
    
    degrees = {
        'phd': ['ph.d', 'phd', 'doctorate', 'doctoral'],
        'masters': ['master', 'msc', 'm.sc', 'ma', 'm.a', 'mba', 'm.b.a', 'mtech', 'm.tech'],
        'bachelors': ['bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'btech', 'b.tech', 'be', 'b.e'],
        'associates': ['associate', 'diploma', 'certification']
    }
    
    found_degrees = []
    for degree_type, variations in degrees.items():
        for variation in variations:
            if variation in text_lower:
                found_degrees.append(degree_type)
                break
    
    # Extract institutions (basic pattern matching)
    institution_patterns = [
        r'university of \w+',
        r'\w+ university',
        r'\w+ college',
        r'\w+ institute'
    ]
    
    institutions = []
    for pattern in institution_patterns:
        matches = re.findall(pattern, text_lower)
        institutions.extend(matches)
    
    return {
        'degrees': list(set(found_degrees)),
        'institutions': list(set(institutions))
    }
