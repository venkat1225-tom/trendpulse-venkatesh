import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches   # used to build the scatter legend manually

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_CSV  = "data/trends_analysed.csv"
OUTPUT_DIR = "outputs"

# Colour palette — one distinct colour per category (used in chart 2)
CATEGORY_COLOURS = {
    "technology":    "#4C72B0",
    "worldnews":     "#DD8452",
    "sports":        "#55A868",
    "science":       "#C44E52",
    "entertainment": "#8172B2",
}

# Colours for popular vs non-popular dots in the scatter plot (chart 3)
POPULAR_COLOUR     = "#E63946"   # bold red  — above-average score
UNPOPULAR_COLOUR   = "#A8DADC"   # soft teal — below-average score

# ---------------------------------------------------------------------------
# Step 1 — Setup: load data and create output folder
# ---------------------------------------------------------------------------

def setup():
    """
    Load the analysed CSV from Task 3 and create the outputs/ directory.
    Returns the DataFrame.
    """
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} rows from {INPUT_CSV}")

    # Create outputs/ folder if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output folder ready: {OUTPUT_DIR}/")

    return df


# ---------------------------------------------------------------------------
# Helper: shorten long titles for y-axis labels
# ---------------------------------------------------------------------------

def shorten(title, max_len=50):
    """Truncate a title to max_len characters, appending '…' if cut."""
    return title if len(title) <= max_len else title[:max_len] + "…"


# ---------------------------------------------------------------------------
# Step 2 — Chart 1: Top 10 Stories by Score (horizontal bar)
# ---------------------------------------------------------------------------

def chart1_top_stories(df):
    """
    Horizontal bar chart of the 10 highest-scoring stories.
    Long titles are shortened so they don't overflow the axis.
    """

    # Sort descending and take the top 10
    top10 = df.nlargest(10, "score").copy()
    top10["short_title"] = top10["title"].apply(shorten)

    # Reverse the order so the highest score appears at the top of the chart
    top10 = top10.iloc[::-1]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Use a sequential colour map so bars fade from light to dark with rank
    colours = plt.cm.Blues_r([i / 10 for i in range(10)])

    ax.barh(top10["short_title"], top10["score"], color=colours, edgecolor="white")

    # Annotate each bar with its exact score
    for i, (score, y) in enumerate(zip(top10["score"], top10["short_title"])):
        ax.text(score + 50, i, f"{score:,}", va="center", fontsize=9)

    ax.set_title("Top 10 Stories by Score", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Score (upvotes)", fontsize=11)
    ax.set_ylabel("Story Title", fontsize=11)
    ax.tick_params(axis="y", labelsize=9)

    plt.tight_layout()

    # savefig BEFORE show — guarantees the file is written even in headless envs
    path = os.path.join(OUTPUT_DIR, "chart1_top_stories.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved {path}")
    plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Step 3 — Chart 2: Stories per Category (bar chart)
# ---------------------------------------------------------------------------

def chart2_categories(df):
    """
    Vertical bar chart showing how many stories landed in each category.
    Each bar gets its own colour from CATEGORY_COLOURS.
    """

    # Count stories per category and sort alphabetically for consistency
    counts = df["category"].value_counts().sort_index()

    # Build the colour list in the same order as the sorted index
    bar_colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in counts.index]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(counts.index, counts.values, color=bar_colours, edgecolor="white",
                  width=0.6)

    # Label each bar with its count above the bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.3,
                str(int(height)), ha="center", va="bottom", fontsize=11)

    ax.set_title("Stories Collected per Category", fontsize=14,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Number of Stories", fontsize=11)
    ax.set_ylim(0, counts.max() + 4)   # a bit of headroom above the tallest bar
    ax.tick_params(axis="x", labelsize=10)

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart2_categories.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved {path}")
    plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Step 4 — Chart 3: Score vs Comments Scatter (coloured by is_popular)
# ---------------------------------------------------------------------------

def chart3_scatter(df):
    """
    Scatter plot: x = score, y = num_comments.
    Dots are coloured red if is_popular == True, teal otherwise.
    A manual legend is built with mpatches so it reads clearly.
    """

    # Split into two subsets for separate plotting calls
    popular     = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    fig, ax = plt.subplots(figsize=(9, 6))

    # Plot non-popular first so popular dots render on top
    ax.scatter(not_popular["score"], not_popular["num_comments"],
               color=UNPOPULAR_COLOUR, alpha=0.7, edgecolors="white",
               linewidths=0.5, s=60, label="Not popular")

    ax.scatter(popular["score"], popular["num_comments"],
               color=POPULAR_COLOUR, alpha=0.85, edgecolors="white",
               linewidths=0.5, s=80, label="Popular (above avg score)")

    # Manual legend patches — clearer than the default scatter legend markers
    legend_handles = [
        mpatches.Patch(color=POPULAR_COLOUR,   label="Popular (above avg score)"),
        mpatches.Patch(color=UNPOPULAR_COLOUR, label="Not popular"),
    ]
    ax.legend(handles=legend_handles, fontsize=10, loc="upper left")

    ax.set_title("Score vs Number of Comments", fontsize=14,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Score (upvotes)", fontsize=11)
    ax.set_ylabel("Number of Comments", fontsize=11)

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "chart3_scatter.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved {path}")
    plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Bonus — Dashboard: all 3 charts in a single figure
# ---------------------------------------------------------------------------

def dashboard(df):
    """
    Reproduce all three charts side-by-side inside one figure.
    Using subplots(1, 3) with a wide figsize keeps things readable.
    """

    fig, axes = plt.subplots(1, 3, figsize=(22, 7))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.01)

    # ---- Panel 1: Top 10 stories (horizontal bar) ----
    top10 = df.nlargest(10, "score").copy()
    top10["short_title"] = top10["title"].apply(shorten)
    top10 = top10.iloc[::-1]   # highest at the top

    colours = plt.cm.Blues_r([i / 10 for i in range(10)])
    axes[0].barh(top10["short_title"], top10["score"],
                 color=colours, edgecolor="white")
    axes[0].set_title("Top 10 Stories by Score", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Score")
    axes[0].set_ylabel("Story Title")
    axes[0].tick_params(axis="y", labelsize=7)

    # ---- Panel 2: Stories per category (vertical bar) ----
    counts      = df["category"].value_counts().sort_index()
    bar_colours = [CATEGORY_COLOURS.get(cat, "#999999") for cat in counts.index]

    axes[1].bar(counts.index, counts.values, color=bar_colours,
                edgecolor="white", width=0.6)
    axes[1].set_title("Stories per Category", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis="x", labelsize=9)

    # ---- Panel 3: Score vs comments scatter ----
    popular     = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                    color=UNPOPULAR_COLOUR, alpha=0.7, s=40,
                    edgecolors="white", linewidths=0.4)
    axes[2].scatter(popular["score"], popular["num_comments"],
                    color=POPULAR_COLOUR, alpha=0.85, s=55,
                    edgecolors="white", linewidths=0.4)

    legend_handles = [
        mpatches.Patch(color=POPULAR_COLOUR,   label="Popular"),
        mpatches.Patch(color=UNPOPULAR_COLOUR, label="Not popular"),
    ]
    axes[2].legend(handles=legend_handles, fontsize=8)
    axes[2].set_title("Score vs Comments", fontsize=11, fontweight="bold")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "dashboard.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved {path}")
    plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== TrendPulse Task 4 – Visualisations ===\n")

    df = setup()

    print("\nGenerating Chart 1 — Top 10 Stories by Score...")
    chart1_top_stories(df)

    print("\nGenerating Chart 2 — Stories per Category...")
    chart2_categories(df)

    print("\nGenerating Chart 3 — Score vs Comments Scatter...")
    chart3_scatter(df)

    print("\nGenerating Bonus Dashboard...")
    dashboard(df)

    print("\nAll done! Check the outputs/ folder for your PNG files.")
