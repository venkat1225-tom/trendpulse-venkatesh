import os
import glob
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Output path for the cleaned CSV (used by Task 3)
OUTPUT_CSV = "data/trends_clean.csv"

# Minimum score a story must have to be kept (low-quality filter)
MIN_SCORE = 5

# ---------------------------------------------------------------------------
# Step 1 — Load the JSON file produced by Task 1
# ---------------------------------------------------------------------------

def load_json(data_dir="data"):
    """
    Find the most recent `trends_YYYYMMDD.json` file in `data/` and
    load it into a Pandas DataFrame.

    Using glob lets the script work regardless of the exact date in
    the filename, so you don't have to hard-code it.
    """

    # Find all files matching the Task 1 naming pattern
    pattern = os.path.join(data_dir, "trends_????????.json")
    matches = sorted(glob.glob(pattern))   # sorted → most recent is last

    if not matches:
        raise FileNotFoundError(
            f"No trends JSON file found in '{data_dir}/'. "
            "Run task1_data_collection.py first."
        )

    # Pick the most recently dated file in case there are several
    filepath = matches[-1]

    # read_json with orient='records' expects a flat list of dicts —
    # exactly what Task 1 produces
    df = pd.read_json(filepath, orient="records")

    print(f"Loaded {len(df)} stories from {filepath}")
    return df


# ---------------------------------------------------------------------------
# Step 2 — Clean the data
# ---------------------------------------------------------------------------

def clean_data(df):
    """
    Apply five cleaning passes to the raw DataFrame and print the row
    count after each pass so progress is visible.
    """

    # --- 2a. Remove duplicate post_ids -----------------------------------
    # HackerNews occasionally returns the same story ID more than once
    # if a story appears near a category boundary.
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # --- 2b. Drop rows with missing critical fields ----------------------
    # A story without a post_id, title, or score is not usable downstream.
    # `dropna` treats empty strings as valid, so we also replace "" with NaN
    # for the title column before dropping.
    df["title"] = df["title"].replace("", pd.NA)          # blank title → NaN
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # --- 2c. Enforce correct data types ----------------------------------
    # JSON numbers may come in as floats (e.g. 42.0) if any nulls were
    # present before the dropna above.  Cast both numeric columns to int.
    df["score"]        = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)
    # post_id should also be a clean integer, not a float
    df["post_id"]      = df["post_id"].astype(int)

    # --- 2d. Remove low-quality stories (score < 5) ----------------------
    # Stories with very few upvotes add noise and are unlikely to be
    # genuinely "trending".
    df = df[df["score"] >= MIN_SCORE]
    print(f"After removing low scores: {len(df)}")

    # --- 2e. Strip leading / trailing whitespace from titles -------------
    # Some titles fetched from the API have stray spaces at the edges.
    df["title"] = df["title"].str.strip()

    return df


# ---------------------------------------------------------------------------
# Step 3 — Save as CSV and print summary
# ---------------------------------------------------------------------------

def save_csv(df, output_path=OUTPUT_CSV):
    """
    Write the cleaned DataFrame to a CSV file and print:
      • a confirmation line with the row count
      • a per-category story count
    """

    # Make sure the output directory exists (it should from Task 1, but
    # better to be safe when running tasks independently)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # index=False keeps the CSV clean — no extra row-number column
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} rows to {output_path}")

    # Per-category summary — value_counts preserves natural sort order,
    # sort=True (default) puts the highest count first
    print("\nStories per category:")
    category_counts = df["category"].value_counts().sort_index()
    for category, count in category_counts.items():
        # Left-align category name in a 16-char field for neat columns
        print(f"  {category:<16}: {count}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== TrendPulse Task 2 – Data Cleaning ===\n")

    # Load → clean → save (each function prints its own progress lines)
    df_raw     = load_json()
    print()                         # blank line before cleaning output
    df_clean   = clean_data(df_raw)
    save_csv(df_clean)
