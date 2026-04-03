import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load data
df = pd.read_csv("cleaned_jobs.csv")

# Extract skills
all_skills = []
for skill_list in df["skills"]:
    all_skills.extend(skill_list.split(", "))

skill_counts = Counter(all_skills)

# Sort skills by demand
sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

skills = [item[0].upper() for item in sorted_skills]
counts = [item[1] for item in sorted_skills]

# Plot
plt.figure(figsize=(10, 6))
bars = plt.bar(skills, counts)

# Add colors
colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336"]
for bar, color in zip(bars, colors):
    bar.set_color(color)

# Add value labels on top
for i, value in enumerate(counts):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=10)

# Titles and labels
plt.title("📊 Job Market Skill Demand Analysis", fontsize=14, fontweight='bold')
plt.xlabel("Skills", fontsize=12)
plt.ylabel("Demand Count", fontsize=12)

plt.xticks(rotation=30)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
