"""
TrendPulse - Task 2: Data Cleaning and CSV Export

This script:
1. Loads JSON data from Task 1
2. Cleans the dataset (duplicates, nulls, types, etc.)
3. Saves the cleaned data as a CSV file

Author: Your Name
"""

import pandas as pd
import os


def main():
    # -------------------------------
    # Step 1: Load JSON file
    # -------------------------------
    file_path = "data/trends_20260403.json"   # ✅ Updated file name

    try:
        df = pd.read_json(file_path)
        print(f"Loaded {len(df)} stories from {file_path}")
    except Exception as e:
        print("Error loading file:", e)
        return

    # -------------------------------
    # Step 2: Clean the Data
    # -------------------------------

    # 1. Remove duplicates based on post_id
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # 2. Remove rows with missing critical values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 3. Convert data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # 4. Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Clean whitespace in title
    df["title"] = df["title"].str.strip()

    # -------------------------------
    # Step 3: Save cleaned data
    # -------------------------------

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    output_file = "data/trends_clean.csv"
    df.to_csv(output_file, index=False)

    print(f"\nSaved {len(df)} rows to {output_file}")

    # -------------------------------
    # Summary: Stories per category
    # -------------------------------
    print("\nStories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()
