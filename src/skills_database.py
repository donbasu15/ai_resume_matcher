"""
Comprehensive skills database for better skill matching
"""

TECHNICAL_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'matlab', 'perl', 'shell', 'bash', 'powershell',
        'sql', 'plsql', 'nosql', 'html', 'css', 'sass', 'scss', 'less'
    ],
    
    'web_frameworks': [
        'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt.js', 'gatsby',
        'django', 'flask', 'fastapi', 'express', 'node.js', 'spring', 'spring boot',
        'laravel', 'symfony', 'rails', 'asp.net', 'blazor'
    ],
    
    'databases': [
        'mysql', 'postgresql', 'sqlite', 'mongodb', 'redis', 'elasticsearch',
        'cassandra', 'dynamodb', 'oracle', 'sql server', 'mariadb', 'neo4j',
        'influxdb', 'couchdb', 'firebase'
    ],
    
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'vercel', 'netlify',
        'digitalocean', 'linode', 'ibm cloud', 'oracle cloud'
    ],
    
    'devops_tools': [
        'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
        'terraform', 'ansible', 'puppet', 'chef', 'vagrant', 'nginx',
        'apache', 'prometheus', 'grafana', 'elk stack', 'splunk'
    ],
    
    'ml_ai': [
        'machine learning', 'deep learning', 'neural networks', 'tensorflow',
        'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'opencv',
        'nlp', 'computer vision', 'reinforcement learning', 'transformers',
        'bert', 'gpt', 'langchain', 'hugging face'
    ],
    
    'data_science': [
        'data analysis', 'data visualization', 'statistics', 'tableau',
        'power bi', 'jupyter', 'spark', 'hadoop', 'kafka',
        'airflow', 'dbt', 'snowflake', 'databricks'
    ],
    
    'mobile_development': [
        'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic',
        'swift', 'objective-c', 'kotlin', 'java'
    ],
    
    'testing': [
        'unit testing', 'integration testing', 'selenium', 'cypress',
        'jest', 'pytest', 'junit', 'testng', 'postman', 'api testing'
    ],
    
    'version_control': [
        'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial'
    ]
}

SOFT_SKILLS = [
    'leadership', 'communication', 'teamwork', 'problem solving',
    'analytical thinking', 'creativity', 'adaptability', 'time management',
    'project management', 'critical thinking', 'collaboration',
    'presentation skills', 'mentoring', 'coaching', 'negotiation',
    'customer service', 'attention to detail', 'multitasking',
    'decision making', 'strategic thinking', 'innovation',
    'emotional intelligence', 'conflict resolution'
]

CERTIFICATIONS = [
    'aws certified', 'azure certified', 'google cloud certified',
    'pmp', 'scrum master', 'product owner', 'cissp', 'cisa',
    'ceh', 'comptia', 'cisco certified', 'oracle certified',
    'microsoft certified', 'salesforce certified', 'kubernetes certified'
]

INDUSTRIES = [
    'fintech', 'healthcare', 'e-commerce', 'education', 'gaming',
    'automotive', 'aerospace', 'telecommunications', 'retail',
    'manufacturing', 'logistics', 'real estate', 'media',
    'entertainment', 'government', 'non-profit', 'consulting'
]

def get_all_skills():
    """Return all technical skills as a flat list."""
    all_skills = []
    for category in TECHNICAL_SKILLS.values():
        all_skills.extend(category)
    all_skills.extend(SOFT_SKILLS)
    all_skills.extend(CERTIFICATIONS)
    return list(set(all_skills))

def get_skills_by_category():
    """Return skills organized by category."""
    return {
        **TECHNICAL_SKILLS,
        'soft_skills': SOFT_SKILLS,
        'certifications': CERTIFICATIONS
    }

def get_skill_synonyms():
    """Return common synonyms for skills."""
    return {
        'javascript': ['js', 'node.js', 'nodejs'],
        'python': ['py'],
        'machine learning': ['ml', 'artificial intelligence', 'ai'],
        'deep learning': ['dl', 'neural networks', 'nn'],
        'natural language processing': ['nlp'],
        'computer vision': ['cv', 'image processing'],
        'user interface': ['ui'],
        'user experience': ['ux'],
        'application programming interface': ['api'],
        'structured query language': ['sql'],
        'cascading style sheets': ['css'],
        'hypertext markup language': ['html'],
        'amazon web services': ['aws'],
        'google cloud platform': ['gcp', 'google cloud'],
        'microsoft azure': ['azure'],
        'continuous integration': ['ci'],
        'continuous deployment': ['cd'],
        'test driven development': ['tdd'],
        'object oriented programming': ['oop'],
        'representational state transfer': ['rest', 'restful'],
        'graphql': ['graph ql'],
        'kubernetes': ['k8s'],
        'elasticsearch': ['elastic search']
    }