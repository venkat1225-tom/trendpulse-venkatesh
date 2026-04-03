import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

print("NEW VERSION RUNNING")  # test line

sns.set_style("whitegrid")

df = pd.read_csv("cleaned_jobs.csv")

all_skills = []
for skill_list in df["skills"]:
    all_skills.extend(skill_list.split(", "))

skill_counts = Counter(all_skills)

sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

skills = [item[0].upper() for item in sorted_skills]
counts = [item[1] for item in sorted_skills]

plt.clf()
plt.figure(figsize=(10, 6))

sns.barplot(x=skills, y=counts)

for i, v in enumerate(counts):
    plt.text(i, v + 0.1, str(v), ha='center')

plt.title("🔥 Job Market Skill Demand (Enhanced)", fontsize=14)
plt.xlabel("Skills")
plt.ylabel("Demand")

plt.tight_layout()
plt.show()
