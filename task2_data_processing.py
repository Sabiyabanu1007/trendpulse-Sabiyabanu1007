import os
import json
import glob
import pandas as pd

def process_and_clean_data():
    # Find latest trends json file
    json_files = glob.glob("data/trends_*.json")
    if not json_files:
        print("Error: No data JSON files found in data/")
        return

    latest_file = max(json_files, key=os.path.getmtime)
    print(f"Loaded {len(json_files)} stories from {latest_file}")

    with open(latest_file, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    if df.empty:
        print("Dataframe is empty!")
        return

    # Drop missing values in essential columns
    df = df.dropna(subset=["id", "title", "score"])

    # Remove duplicates based on story id
    df = df.drop_duplicates(subset=["id"])
    print(f"After removing duplicates: {len(df)}")

    # Clean text columns
    df["title"] = df["title"].astype(str).str.strip()

    # Fill missing values for scores and comments
    df["score"] = df["score"].fillna(0).astype(int)
    if "comments_count" in df.columns:
        df["comments_count"] = df["comments_count"].fillna(0).astype(int)
    elif "num_comments" in df.columns:
        df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Filter out stories with score less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Save as CSV
    os.makedirs("data", exist_ok=True)
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    process_and_clean_data()