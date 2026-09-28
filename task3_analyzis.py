import os
import numpy as np
import pandas as pd


def analyze_data():
    file_path = "data/trends_clean.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist!")
        return

    # 1. Load data/trends_clean.csv into Pandas DataFrame
    df = pd.read_csv(file_path)

    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"\nAverage score    : {avg_score:.3f}")
    print(f"Average comments : {avg_comments:.3f}")

    # 2. Basic Analysis with NumPy
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print("\n--- NumPy Stats ---")
    print(f"Mean score     : {mean_score:.3f}")
    print(f"Median score   : {median_score:.3f}")
    print(f"Std deviation  : {std_score:.3f}")
    print(f"Max score      : {max_score}")
    print(f"Min score      : {min_score}")

    # Top category
    top_cat = df["category"].value_counts().idxmax()
    top_cat_count = df["category"].value_counts().max()
    print(f"\nMost stories in: {top_cat} ({top_cat_count} stories)")

    # Most commented story
    most_commented_idx = df["num_comments"].idxmax()
    most_commented_story = df.loc[most_commented_idx]
    print(
        f'Most commented story: "{most_commented_story["title"]}" - {most_commented_story["num_comments"]} comments'
    )

    # 3. Add New Columns
    # engagement = num_comments / (score + 1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = boolean flag (score > median AND num_comments > median)
    median_comm = np.median(comments)
    df["is_popular"] = (df["score"] > median_score) & (
        df["num_comments"] > median_comm
    )

    # 4. Save to CSV
    os.makedirs("data", exist_ok=True)
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    analyze_data()