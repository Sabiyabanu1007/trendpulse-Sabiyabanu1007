import os
import pandas as pd
import matplotlib.pyplot as plt

def create_visualizations():
    # 1. Load data and setup
    file_path = "data/trends_analysed.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist!")
        return

    df = pd.read_csv(file_path)
    os.makedirs("outputs", exist_ok=True)

    # Determine comment column dynamically
    comment_col = "comments_count" if "comments_count" in df.columns else "num_comments"

    # Category handling (creates pseudo-categories based on score if missing)
    if "category" not in df.columns:
        df["category"] = pd.cut(df["score"], bins=[-1, 50, 200, 10000], labels=["Low Score", "Medium Score", "High Score"])

    # Popularity classification for scatter plot
    median_score = df["score"].median()
    df["popularity"] = df["score"].apply(lambda x: "Popular" if x >= median_score else "Non-Popular")

    # ==========================================
    # CHART 1: Top Stories Horizontal Bar Chart
    # ==========================================
    plt.figure(figsize=(10, 6))
    top_10 = df.sort_values(by="score", ascending=False).head(10)
    shortened_titles = [t[:40] + "..." if len(t) > 40 else t for t in top_10["title"]]
    
    plt.barh(shortened_titles[::-1], top_10["score"][::-1], color="skyblue")
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Chart 1: Top 10 Stories by Score")
    plt.tight_layout()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()

    # ==========================================
    # CHART 2: Stories Per Category Bar Chart
    # ==========================================
    plt.figure(figsize=(8, 5))
    category_counts = df["category"].value_counts()
    category_counts.plot(kind="bar", color="teal")
    plt.xlabel("Category / Score Range")
    plt.ylabel("Number of Stories")
    plt.title("Chart 2: Stories per Category")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("outputs/chart2_stories_per_category.png")
    plt.close()

    # ==========================================
    # CHART 3: Score vs Comments Scatter Plot
    # ==========================================
    plt.figure(figsize=(8, 6))
    popular = df[df["popularity"] == "Popular"]
    non_popular = df[df["popularity"] == "Non-Popular"]

    plt.scatter(popular["score"], popular[comment_col], color="crimson", label="Popular", alpha=0.7)
    plt.scatter(non_popular["score"], non_popular[comment_col], color="dodgerblue", label="Non-Popular", alpha=0.7)
    
    plt.xlabel("Score")
    plt.ylabel("Comments Count")
    plt.title("Chart 3: Score vs Comments (Popular vs Non-Popular)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/chart3_score_vs_comments.png")
    plt.close()

    # ==========================================
    # BONUS: Combined Dashboard (3-in-1 Chart)
    # ==========================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Hacker News Analytics Dashboard", fontsize=16)

    # Subplot 1
    axes[0, 0].barh(shortened_titles[::-1], top_10["score"][::-1], color="skyblue")
    axes[0, 0].set_title("Top 10 Stories by Score")
    axes[0, 0].set_xlabel("Score")

    # Subplot 2
    category_counts.plot(kind="bar", ax=axes[0, 1], color="teal")
    axes[0, 1].set_title("Stories per Category")
    axes[0, 1].set_xlabel("Category")
    axes[0, 1].set_ylabel("Count")

    # Subplot 3
    axes[1, 0].scatter(popular["score"], popular[comment_col], color="crimson", label="Popular", alpha=0.7)
    axes[1, 0].scatter(non_popular["score"], non_popular[comment_col], color="dodgerblue", label="Non-Popular", alpha=0.7)
    axes[1, 0].set_title("Score vs Comments")
    axes[1, 0].set_xlabel("Score")
    axes[1, 0].set_ylabel("Comments")
    axes[1, 0].legend()

    # Hide extra blank 4th subplot
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig("outputs/combined_dashboard.png")
    plt.close()

    print("All 3 Charts + Bonus Combined Dashboard created successfully in outputs/ folder!")

if __name__ == "__main__":
    create_visualizations()