import requests
import json
import os
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# HackerNews API base URL
BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Browser-like User-Agent header as required by the task spec
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Maximum stories to collect per category (125 total across 5 categories)
MAX_PER_CATEGORY = 25

# Number of top story IDs to pull from HackerNews
TOP_STORIES_LIMIT = 500

# Keyword map: each category maps to a list of case-insensitive keywords
CATEGORY_KEYWORDS = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data",
                      "cloud", "api", "gpu", "llm"],
    "worldnews":     ["war", "government", "country", "president", "election",
                      "climate", "attack", "global"],
    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team", "player",
                      "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology",
                      "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book",
                      "show", "award", "streaming"],
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def fetch_top_story_ids(limit=TOP_STORIES_LIMIT):
    """
    Fetch the list of current top story IDs from HackerNews.
    Returns the first `limit` IDs as a list of integers.
    Returns an empty list if the request fails.
    """
    url = f"{BASE_URL}/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()           # raises on 4xx / 5xx
        ids = response.json()
        print(f"Fetched {len(ids)} story IDs. Using first {limit}.")
        return ids[:limit]
    except requests.RequestException as e:
        print(f"[ERROR] Could not fetch top story IDs: {e}")
        return []


def fetch_story(story_id):
    """
    Fetch a single story object from HackerNews by its ID.
    Returns the parsed JSON dict, or None if the request fails.
    """
    url = f"{BASE_URL}/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Don't crash – just warn and return None so the caller can skip
        print(f"[WARNING] Could not fetch story {story_id}: {e}")
        return None


def assign_category(title):
    """
    Check a story title against each category's keyword list.
    Returns the first matching category name, or None if no match.
    Comparison is case-insensitive.
    """
    if not title:
        return None

    lower_title = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in lower_title:
                return category

    return None  # title didn't match any category


def extract_fields(story, category):
    """
    Pull the 7 required fields out of a raw HackerNews story dict.
    `collected_at` is added here using the current UTC timestamp.
    """
    return {
        "post_id":       story.get("id"),
        "title":         story.get("title", ""),
        "category":      category,
        "score":         story.get("score", 0),
        "num_comments":  story.get("descendants", 0),   # HN calls it `descendants`
        "author":        story.get("by", ""),
        "collected_at":  datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

# ---------------------------------------------------------------------------
# Main collection logic
# ---------------------------------------------------------------------------

def collect_stories():
    """
    Main pipeline:
      1. Fetch top story IDs
      2. Iterate through stories, categorise, and collect up to 25 per category
      3. Sleep 2 seconds after finishing each category bucket
      4. Return a flat list of story dicts
    """

    # Step 1 – get the pool of story IDs to work with
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("[ERROR] No story IDs retrieved. Exiting.")
        return []

    # Bucket to hold collected stories, keyed by category
    collected = {category: [] for category in CATEGORY_KEYWORDS}

    # Step 2 – iterate through story IDs and fill the buckets
    for story_id in story_ids:

        # Stop early if every category is already full
        if all(len(stories) >= MAX_PER_CATEGORY for stories in collected.values()):
            print("All category buckets are full. Stopping early.")
            break

        # Fetch the raw story object
        story = fetch_story(story_id)
        if story is None:
            continue   # fetch failed – skip this ID

        # Only process stories (not jobs, polls, etc.) that have a title
        if story.get("type") != "story" or not story.get("title"):
            continue

        # Determine which category this story belongs to
        category = assign_category(story["title"])
        if category is None:
            continue   # no keyword match – not useful for TrendPulse

        # Skip if we've already hit the cap for this category
        if len(collected[category]) >= MAX_PER_CATEGORY:
            continue

        # Extract the 7 required fields and add to the bucket
        story_data = extract_fields(story, category)
        collected[category].append(story_data)

        # Sleep 2 seconds each time a category bucket becomes full
        # (one sleep per completed category, not per individual story fetch)
        if len(collected[category]) == MAX_PER_CATEGORY:
            print(f"  Category '{category}' complete "
                  f"({MAX_PER_CATEGORY} stories). Sleeping 2 s...")
            time.sleep(2)

    # Flatten the per-category buckets into a single list
    all_stories = [story for bucket in collected.values() for story in bucket]

    # Print a summary of how many stories landed in each category
    print("\n--- Collection Summary ---")
    for category, bucket in collected.items():
        print(f"  {category:<15}: {len(bucket)} stories")
    print(f"  {'TOTAL':<15}: {len(all_stories)} stories")

    return all_stories


# ---------------------------------------------------------------------------
# File saving
# ---------------------------------------------------------------------------

def save_to_json(stories):
    """
    Save the collected stories list to `data/trends_YYYYMMDD.json`.
    Creates the `data/` directory if it doesn't already exist.
    Prints the path and story count on success.
    """

    # Create the output directory if needed
    os.makedirs("data", exist_ok=True)

    # Build a date-stamped filename (matches the expected format)
    date_str = datetime.utcnow().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    print(f"\nCollected {len(stories)} stories. Saved to {filename}")
    return filename


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== TrendPulse Task 1 – Data Collection ===\n")

    stories = collect_stories()

    if len(stories) < 100:
        print(f"\n[WARNING] Only {len(stories)} stories collected "
              "(target is at least 100). HackerNews may have fewer "
              "matching stories right now.")

    save_to_json(stories)
