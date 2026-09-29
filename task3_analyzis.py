import os
import pandas as pd

def analyze_trends():
    file_path = "data/trends_clean.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist!")
        return

    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")

    # Check for correct comments column name
    comment_col = "comments_count" if "comments_count" in df.columns else "num_comments"

    # Calculate statistics
    avg_score = df["score"].mean()
    avg_comments = df[comment_col].mean()

    print(f"Average Score: {avg_score:.2f}")
    print(f"Average Comments: {avg_comments:.2f}")

    # Top stories analysis
    top_by_score = df.sort_values(by="score", ascending=False).head(10)
    top_by_comments = df.sort_values(by=comment_col, ascending=False).head(10)

    # Save analysed data
    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)
    print(f"Analysis complete. Saved to {output_path}")

if __name__ == "__main__":
    analyze_trends()