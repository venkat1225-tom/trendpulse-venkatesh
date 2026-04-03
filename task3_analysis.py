"""
TrendPulse - Task 3: Data Analysis using Pandas & NumPy

This script:
1. Loads cleaned CSV data from Task 2
2. Performs analysis using Pandas and NumPy
3. Adds new calculated columns
4. Saves the updated dataset for visualization

Author: Your Name
"""

import pandas as pd
import numpy as np
import os


def main():
    # -------------------------------
    # Step 1: Load and Explore Data
    # -------------------------------
    file_path = "data/trends_clean.csv"

    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data: {df.shape}")
    except Exception as e:
        print("Error loading file:", e)
        return

    # Print first 5 rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Average values using Pandas
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # -------------------------------
    # Step 2: Analysis using NumPy
    # -------------------------------
    scores = df["score"].to_numpy()

    print("\n--- NumPy Stats ---")
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Std deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_count = category_counts.max()

    print(f"\nMost stories in: {top_category} ({top_count} stories)")

    # Story with most comments
    max_comments_row = df.loc[df["num_comments"].idxmax()]
    print(f"\nMost commented story:")
    print(f"\"{max_comments_row['title']}\" — {max_comments_row['num_comments']} comments")

    # -------------------------------
    # Step 3: Add New Columns
    # -------------------------------

    # Engagement = comments per score
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # Popular if score > average score
    df["is_popular"] = df["score"] > avg_score

    # -------------------------------
    # Step 4: Save the Result
    # -------------------------------
    output_file = "data/trends_analysed.csv"
    df.to_csv(output_file, index=False)

    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()
