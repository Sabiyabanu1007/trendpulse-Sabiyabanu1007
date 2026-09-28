import glob
import os
import pandas as pd


def process_and_clean_data():
    # Find the JSON file inside data/ folder
    json_files = glob.glob("data/trends_*.json")
    if not json_files:
        print("No JSON file found in data/ folder!")
        return

    latest_json = json_files[0]

    # 1. Load the JSON File into DataFrame
    df = pd.read_json(latest_json)
    print(f"Loaded {len(df)} stories from {latest_json}")

    # 2. Clean the Data
    # Remove duplicate post_ids
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # Drop rows where post_id, title, or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Clean whitespace in title column
    df["title"] = df["title"].astype(str).str.strip()

    # Ensure score and num_comments are integers
    df["score"] = df["score"].fillna(0).astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Filter out stories with score less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 3. Save as CSV
    os.makedirs("data", exist_ok=True)
    output_csv = "data/trends_clean.csv"
    df.to_csv(output_csv, index=False)
    print(f"\nSaved {len(df)} rows to {output_csv}")

    # Print quick summary: stories per category
    if "category" in df.columns:
        print("\nStories per category:")
        category_counts = df["category"].value_counts()
        for cat, count in category_counts.items():
            print(f"  {cat:<15} {count}")


if __name__ == "__main__":
    process_and_clean_data()