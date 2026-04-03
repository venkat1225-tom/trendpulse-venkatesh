import requests
import pandas as pd

url = "https://remotive.com/api/remote-jobs"

response = requests.get(url)
data = response.json()

jobs = []

for job in data["jobs"][:50]:  # limit to 50
    jobs.append({
        "title": job["title"],
        "company": job["company_name"],
        "category": job["category"],
        "salary": job["salary"],
        "description": job["description"]
    })

df = pd.DataFrame(jobs)
df.to_csv("raw_jobs.csv", index=False)

print("✅ Data collected and saved as raw_jobs.csv")
