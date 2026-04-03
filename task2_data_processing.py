"""
TrendPulse - Task 2: Data Cleaning and CSV Export

This script:
1. Loads JSON data from Task 1
2. Cleans the dataset (duplicates, nulls, types, etc.)
3. Saves the cleaned data as a CSV file

Author: venkatesh
"""

import pandas as pd
import os

# File path (make sure JSON exists from Task 1)
INPUT_FILE = "data/trends_20240115.json"   # <-- change date if needed
OUTPUT_FILE = "data/trends_clean.csv"


def main():
    # -------------------------------
    # Step 1: Load JSON into DataFrame
    # -------------------------------
    try:
        df = pd.read_json(INPUT_FILE)
        print(f"Loaded {len(df)} stories from {INPUT_FILE}")
    except Exception as e:
        print("Error loading JSON file:", e)
        return

    # -------------------------------
    # Step 2: Clean the Data
    # -------------------------------

    # 1. Remove duplicates based on post_id
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # 2. Remove rows with missing critical values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 3. Convert data types
    # Sometimes values might be float or string, so force conversion
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # 4. Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Clean whitespace in title
    df["title"] = df["title"].str.strip()

    # -------------------------------
    # Step 3: Save as CSV
    # -------------------------------

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved {len(df)} rows to {OUTPUT_FILE}")

    # -------------------------------
    # Summary: Stories per category
    # -------------------------------
    print("\nStories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()
