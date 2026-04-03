import pandas as pd
import re

df = pd.read_csv("raw_jobs.csv")

# Remove duplicates & nulls
df = df.drop_duplicates()
df = df.dropna()

# Skill keywords
skills = ["python", "sql", "java", "aws", "excel", "power bi"]

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in skills if skill in text]
    return ", ".join(found)

df["skills"] = df["description"].apply(extract_skills)

# Clean empty skill rows
df = df[df["skills"] != ""]

df.to_csv("cleaned_jobs.csv", index=False)

print("✅ Data cleaned and saved as cleaned_jobs.csv")
