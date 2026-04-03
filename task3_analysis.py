import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_CSV  = "data/trends_clean.csv"
OUTPUT_CSV = "data/trends_analysed.csv"

# ---------------------------------------------------------------------------
# Step 1 — Load and Explore
# ---------------------------------------------------------------------------

def load_and_explore(filepath=INPUT_CSV):
    """
    Load the cleaned CSV into a DataFrame and print basic info:
    shape, first 5 rows, and average score / num_comments.
    """

    df = pd.read_csv(filepath)

    # Shape tells us (rows, columns) at a glance
    print(f"Loaded data: {df.shape}")

    print("\nFirst 5 rows:")
    # to_string() avoids truncated column output in narrow terminals
    print(df.head().to_string(index=False))

    # Pandas .mean() gives a quick sanity-check on the numeric columns
    avg_score    = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")

    return df


# ---------------------------------------------------------------------------
# Step 2 — Basic Analysis with NumPy
# ---------------------------------------------------------------------------

def numpy_analysis(df):
    """
    Use NumPy directly (not Pandas wrappers) to compute descriptive
    statistics on `score`, find the range, and surface two category-
    level insights.
    """

    # Pull the score column into a plain NumPy array for explicit use
    scores = df["score"].to_numpy()

    print("\n--- NumPy Stats ---")

    # Central tendency and spread
    mean_score   = np.mean(scores)
    median_score = np.median(scores)
    std_score    = np.std(scores)       # population std (NumPy default)

    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")

    # Range — highest and lowest individual scores
    max_score = np.max(scores)
    min_score = np.min(scores)

    print(f"Max score    : {max_score:,}")
    print(f"Min score    : {min_score:,}")

    # Which category has the most stories?
    # value_counts() on the category column, then pick the top entry
    top_category       = df["category"].value_counts().idxmax()
    top_category_count = df["category"].value_counts().max()

    print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

    # Which single story attracted the most comments?
    # idxmax() returns the DataFrame index of the row with the highest value
    most_commented_idx   = df["num_comments"].idxmax()
    most_commented_row   = df.loc[most_commented_idx]

    print(f'\nMost commented story: "{most_commented_row["title"]}"'
          f'  — {most_commented_row["num_comments"]:,} comments')

    return mean_score   # returned so Step 3 can reuse it without recomputing


# ---------------------------------------------------------------------------
# Step 3 — Add New Derived Columns
# ---------------------------------------------------------------------------

def add_columns(df, avg_score):
    """
    Enrich the DataFrame with two computed columns:

    `engagement`  — comments per upvote (+ 1 to avoid division by zero)
                    High engagement means lots of discussion relative to likes.

    `is_popular`  — True when a story's score is above the dataset average.
                    Useful for quick filtering in Task 4 charts.
    """

    # engagement: how much discussion each upvote tends to generate
    # Adding 1 to the denominator prevents ZeroDivisionError for score == 0
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular: boolean flag — True if score beats the overall mean
    df["is_popular"] = df["score"] > avg_score

    print(f"\nNew columns added: 'engagement', 'is_popular'")
    print(f"Popular stories (score > {avg_score:.0f}): {df['is_popular'].sum()}")

    return df


# ---------------------------------------------------------------------------
# Step 4 — Save the Enriched DataFrame
# ---------------------------------------------------------------------------

def save_csv(df, output_path=OUTPUT_CSV):
    """
    Write the analysed DataFrame (with the two new columns) to CSV.
    index=False keeps the file clean — no extra row-number column.
    """

    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== TrendPulse Task 3 – Analysis ===\n")

    # Step 1: load + basic Pandas exploration
    df = load_and_explore()

    # Step 2: NumPy statistics; returns the mean score for reuse in Step 3
    avg_score = numpy_analysis(df)

    # Step 3: add engagement and is_popular columns
    df = add_columns(df, avg_score)

    # Step 4: persist the enriched DataFrame for Task 4
    save_csv(df)
