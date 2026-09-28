import matplotlib.pyplot as plt
import pandas as pd


def visualize_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        top_coins = df.head(10)

        plt.figure(figsize=(10, 6))
        plt.bar(
            top_coins["name"], top_coins["market_cap_rank"], color="skyblue"
        )
        plt.xlabel("Coin Name")
        plt.ylabel("Market Cap Rank")
        plt.title("Top Trending Coins Rank")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("trending_chart.png")
        print("Chart saved as trending_chart.png!")
    except Exception as e:
        print(f"Error visualizing data: {e}")


if __name__ == "__main__":
    visualize_data()