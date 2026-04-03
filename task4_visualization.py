import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_csv("cleaned_jobs.csv")

all_skills = []

for skill_list in df["skills"]:
    all_skills.extend(skill_list.split(", "))

skill_counts = Counter(all_skills)

skills = list(skill_counts.keys())
counts = list(skill_counts.values())

plt.bar(skills, counts)
plt.title("Job Market Skill Demand")
plt.xlabel("Skills")
plt.ylabel("Demand Count")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
