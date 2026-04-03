import pandas as pd
from collections import Counter

df = pd.read_csv("cleaned_jobs.csv")

all_skills = []

for skill_list in df["skills"]:
    all_skills.extend(skill_list.split(", "))

skill_counts = Counter(all_skills)

print("🔥 Top Skills in Demand:\n")
for skill, count in skill_counts.most_common():
    print(f"{skill}: {count}")
