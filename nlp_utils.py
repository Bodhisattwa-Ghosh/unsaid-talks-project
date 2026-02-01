SKILLS_DB = [
    "python", "java", "c++", "sql", "machine learning",
    "dsa", "data structures", "algorithms",
    "fastapi", "pandas", "numpy", "react"
]

def extract_skills(text: str):
    text = text.lower()
    return [skill.title() for skill in SKILLS_DB if skill in text]




