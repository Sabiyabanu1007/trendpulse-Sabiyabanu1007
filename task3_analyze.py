import pandas as pd


def analyze_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        print("--- DATA ANALYSIS REPORT ---")
        print(f"Total Trending Coins: {len(df)}")
        print(
            f"Highest Ranked Coin: {df.loc[df['market_cap_rank'].idxmin()]['name']}"
        )
        print(
            f"Lowest Ranked Coin: {df.loc[df['market_cap_rank'].idxmax()]['name']}"
        )
        print("\nSummary Statistics:")
        print(df.describe())
    except Exception as e:
        print(f"Error analyzing data: {e}")


if __name__ == "__main__":
    analyze_data()