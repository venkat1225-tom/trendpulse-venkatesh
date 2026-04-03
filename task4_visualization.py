"""
TrendPulse - Task 4: Data Visualization

This script:
1. Loads analysed CSV data
2. Creates 3 charts using matplotlib
3. Saves each chart as PNG
4. Combines charts into a dashboard

Author: venkatesh
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def shorten_title(title, max_length=50):
    """Shorten long titles for better display in charts"""
    return title[:max_length] + "..." if len(title) > max_length else title


def main():
    # -------------------------------
    # Step 1: Load Data & Setup
    # -------------------------------
    file_path = "data/trends_analysed.csv"

    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
    except Exception as e:
        print("Error loading file:", e)
        return

    # Create outputs folder if not exists
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # -------------------------------
    # Chart 1: Top 10 Stories by Score
    # -------------------------------
    top10 = df.sort_values(by="score", ascending=False).head(10)

    titles = [shorten_title(t) for t in top10["title"]]

    plt.figure()
    plt.barh(titles, top10["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()  # highest score on top

    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()

    # -------------------------------
    # Chart 2: Stories per Category
    # -------------------------------
    category_counts = df["category"].value_counts()

    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.savefig("outputs/chart2_categories.png")
    plt.close()

    # -------------------------------
    # Chart 3: Score vs Comments
    # -------------------------------
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.savefig("outputs/chart3_scatter.png")
    plt.close()

    # -------------------------------
    # Bonus: Dashboard
    # -------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1 (Dashboard)
    axes[0].barh(titles, top10["score"])
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2 (Dashboard)
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3 (Dashboard)
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard")

    plt.savefig("outputs/dashboard.png")
    plt.close()

    print("All charts saved in 'outputs/' folder.")


if __name__ == "__main__":
    main()
