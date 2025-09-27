from src.embedding import compute_similarity
from src.extractor import extract_skills, extract_experience_level, extract_education
from src.preprocessing import extract_sections, advanced_text_preprocessing
import re
from collections import Counter

def calculate_keyword_density(text: str, keywords: list) -> dict:
    """Calculate keyword density for important terms."""
    text_lower = text.lower()
    word_count = len(text_lower.split())
    
    density_scores = {}
    for keyword in keywords:
        keyword_lower = keyword.lower()
        count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
        density = (count / word_count) * 100 if word_count > 0 else 0
        density_scores[keyword] = {
            'count': count,
            'density': round(density, 2)
        }
    
    return density_scores

def calculate_section_scores(resume_sections: dict, jd_sections: dict) -> dict:
    """Calculate matching scores for different resume sections."""
    section_scores = {}
    
    # Define weights for different sections
    section_weights = {
        'skills': 0.35,
        'experience': 0.30,
        'education': 0.15,
        'projects': 0.10,
        'certifications': 0.10
    }
    
    for section in section_weights.keys():
        if section in resume_sections and section in jd_sections:
            if resume_sections[section] and jd_sections[section]:
                similarity = compute_similarity(
                    resume_sections[section], 
                    jd_sections[section]
                )
                # Ensure similarity is between 0 and 100
                similarity = max(0, min(100, similarity))
                section_scores[section] = {
                    'score': similarity,
                    'weight': section_weights[section],
                    'weighted_score': (similarity / 100) * section_weights[section]
                }
            else:
                section_scores[section] = {
                    'score': 0,
                    'weight': section_weights[section],
                    'weighted_score': 0
                }
        else:
            section_scores[section] = {
                'score': 0,
                'weight': section_weights[section],
                'weighted_score': 0
            }
    
    return section_scores

def analyze_experience_match(resume_exp: dict, jd_text: str) -> dict:
    """Analyze experience level matching."""
    jd_exp = extract_experience_level(jd_text)
    
    # Calculate experience match score
    resume_max_years = resume_exp.get('max_years', 0)
    jd_max_years = jd_exp.get('max_years', 0)
    
    if jd_max_years == 0:
        years_match = 100  # No specific requirement
    elif resume_max_years >= jd_max_years:
        years_match = 100
    else:
        # Partial credit if close
        if resume_max_years >= jd_max_years * 0.7:
            years_match = 80
        elif resume_max_years >= jd_max_years * 0.5:
            years_match = 60
        else:
            years_match = 40
    
    # Level matching
    resume_levels = set(resume_exp.get('levels_detected', []))
    jd_levels = set(jd_exp.get('levels_detected', []))
    
    if not jd_levels:
        level_match = 100  # No specific level requirement
    else:
        common_levels = resume_levels.intersection(jd_levels)
        level_match = (len(common_levels) / len(jd_levels)) * 100 if jd_levels else 0
    
    return {
        'years_match_score': years_match,
        'level_match_score': level_match,
        'resume_experience': resume_exp,
        'jd_requirements': jd_exp,
        'overall_experience_score': (years_match + level_match) / 2
    }

def generate_improvement_suggestions(resume_skills: dict, jd_skills: dict, 
                                   experience_analysis: dict) -> list:
    """Generate actionable improvement suggestions."""
    suggestions = []
    
    # Skill gaps
    resume_all_skills = set(resume_skills.get('exact_matches', []) + 
                          resume_skills.get('fuzzy_matches', []))
    jd_all_skills = set(jd_skills.get('exact_matches', []) + 
                       jd_skills.get('fuzzy_matches', []))
    
    missing_skills = jd_all_skills - resume_all_skills
    
    if missing_skills:
        # Prioritize missing skills by category
        critical_skills = []
        nice_to_have = []
        
        for skill in missing_skills:
            # Simple prioritization - you can make this more sophisticated
            if any(keyword in skill.lower() for keyword in 
                  ['python', 'java', 'sql', 'aws', 'react', 'machine learning']):
                critical_skills.append(skill)
            else:
                nice_to_have.append(skill)
        
        if critical_skills:
            suggestions.append({
                'type': 'critical_skills',
                'title': 'Critical Skills Missing',
                'description': f"Add these important skills to your resume: {', '.join(critical_skills[:5])}",
                'priority': 'high'
            })
        
        if nice_to_have:
            suggestions.append({
                'type': 'additional_skills',
                'title': 'Additional Skills to Consider',
                'description': f"Consider highlighting these skills if you have them: {', '.join(nice_to_have[:5])}",
                'priority': 'medium'
            })
    
    # Experience suggestions
    exp_score = experience_analysis.get('overall_experience_score', 0)
    if exp_score < 80:
        if experience_analysis.get('years_match_score', 0) < 80:
            suggestions.append({
                'type': 'experience',
                'title': 'Experience Level',
                'description': "Highlight relevant experience more prominently or consider gaining more experience in the required areas",
                'priority': 'high'
            })
    
    # Keyword density suggestions
    if len(resume_all_skills) < len(jd_all_skills) * 0.5:
        suggestions.append({
            'type': 'keywords',
            'title': 'Keyword Optimization',
            'description': "Include more relevant keywords from the job description in your resume",
            'priority': 'medium'
        })
    
    return suggestions

def match_resume(resume_text: str, jd_text: str, skills: list = None):
    """Enhanced resume matching with detailed analysis."""
    
    # Extract sections
    resume_sections = extract_sections(resume_text)
    jd_sections = extract_sections(jd_text)
    
    # Overall similarity
    overall_similarity = compute_similarity(resume_text, jd_text)
    
    # Skill extraction and matching
    resume_skills = extract_skills(resume_text, skills)
    jd_skills = extract_skills(jd_text, skills)
    
    # Calculate skill match score
    resume_all_skills = set(resume_skills.get('exact_matches', []) + 
                          resume_skills.get('fuzzy_matches', []))
    jd_all_skills = set(jd_skills.get('exact_matches', []) + 
                       jd_skills.get('fuzzy_matches', []))
    
    common_skills = resume_all_skills.intersection(jd_all_skills)
    skill_match_score = (len(common_skills) / len(jd_all_skills)) * 100 if jd_all_skills else 100
    
    # Experience analysis
    resume_experience = extract_experience_level(resume_text)
    experience_analysis = analyze_experience_match(resume_experience, jd_text)
    
    # Education analysis
    resume_education = extract_education(resume_text)
    jd_education = extract_education(jd_text)
    
    # Section-wise scoring
    section_scores = calculate_section_scores(resume_sections, jd_sections)
    
    # Calculate weighted overall score
    weights = {
        'semantic_similarity': 0.25,
        'skill_match': 0.35,
        'experience_match': 0.25,
        'section_scores': 0.15
    }
    
    section_weighted_sum = sum(score['weighted_score'] for score in section_scores.values())
    
    final_score = (
        (overall_similarity / 100) * weights['semantic_similarity'] +
        (skill_match_score / 100) * weights['skill_match'] +
        (experience_analysis['overall_experience_score'] / 100) * weights['experience_match'] +
        section_weighted_sum
    ) * 100
    
    # Generate suggestions
    suggestions = generate_improvement_suggestions(
        resume_skills, jd_skills, experience_analysis
    )
    
    # Keyword density analysis
    jd_keywords = list(jd_all_skills)[:10]  # Top keywords from JD
    keyword_density = calculate_keyword_density(resume_text, jd_keywords)
    
    return {
        "overall_match_score": round(final_score, 2),
        "component_scores": {
            "semantic_similarity": round(overall_similarity, 2),
            "skill_match": round(skill_match_score, 2),
            "experience_match": round(experience_analysis['overall_experience_score'], 2),
            "section_scores": section_scores
        },
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "common_skills": list(common_skills),
        "missing_skills": list(jd_all_skills - resume_all_skills),
        "experience_analysis": experience_analysis,
        "education_info": {
            "resume": resume_education,
            "jd": jd_education
        },
        "keyword_density": keyword_density,
        "improvement_suggestions": suggestions,
        "resume_sections": resume_sections
    }
