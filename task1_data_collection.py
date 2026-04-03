"""
TrendPulse - Task 1: Data Collection from HackerNews API

Steps:
1. Fetch top 500 story IDs
2. Fetch story details
3. Categorize stories based on keywords
4. Collect max 25 per category
5. Save to JSON file

Author: venkatesh
"""

import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


def get_category(title):
    """
    Assign category based on keywords in title.
    Returns category name or None.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


def fetch_top_story_ids():
    """
    Fetch top story IDs from HackerNews.
    """
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]  # First 500 IDs
    except Exception as e:
        print("Error fetching top stories:", e)
        return []


def fetch_story(story_id):
    """
    Fetch individual story details.
    """
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def main():
    # Step 1: Fetch IDs
    story_ids = fetch_top_story_ids()

    # Store results
    collected_data = []
    category_counts = {cat: 0 for cat in CATEGORIES}

    # Step 2: Loop through categories
    for category in CATEGORIES:

        for story_id in story_ids:
            # Stop if category is full
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            if not story or "title" not in story:
                continue

            title = story.get("title", "")

            # Check category
            assigned_category = get_category(title)

            if assigned_category != category:
                continue

            # Extract fields
            data = {
                "post_id": story.get("id"),
                "title": title,
                "category": assigned_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(data)
            category_counts[category] += 1

        # Required sleep (per category, not per request)
        time.sleep(2)

    # Step 3: Save JSON
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(collected_data, file, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
