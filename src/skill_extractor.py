import re

# A basic list of skills for extraction. In a real scenario, this would be much more extensive.
SKILLS_DB = [
    'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'php', 'scala', 'rust',
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle', 'redis', 'cassandra',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ansible', 'terraform',
    'react', 'angular', 'vue', 'node.js', 'express', 'flask', 'django', 'fastapi',
    'pandas', 'numpy', 'scipy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'opencv',
    'natural language processing', 'nlp', 'computer vision', 'deep learning', 'machine learning',
    'data analysis', 'data science', 'tableau', 'power bi', 'excel', 'statistics', 'math',
    'agile', 'scrum', 'git', 'github', 'jira', 'confluence', 'rest api', 'graphql',
    'linear regression', 'logistic regression', 'decision tree', 'random forest', 'xgboost',
    'gradient boosting', 'svm', 'knn', 'clustering', 'pca', 'dimensionality reduction',
    'feature engineering', 'time series', 'ab testing', 'eda', 'exploratory data analysis'
]

def extract_skills(text):
    """
    Extract skills from text by matching against a predefined database.
    """
    extracted_skills = []
    text = text.lower()
    
    for skill in SKILLS_DB:
        # Using word boundaries to avoid partial matches (e.g., 'go' in 'good')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            extracted_skills.append(skill)
            
    return list(set(extracted_skills))

def get_missing_skills(resume_skills, jd_skills):
    """
    Compare resume skills with JD skills to find gaps.
    """
    missing = [skill for skill in jd_skills if skill not in resume_skills]
    return missing
