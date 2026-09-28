import json
import pandas as pd


def clean_data():
    try:
        with open("raw_data.json", "r") as f:
            data = json.load(f)

        coins = data.get("coins", [])
        cleaned_list = []

        for item in coins:
            coin = item["item"]
            cleaned_list.append(
                {
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol"),
                    "market_cap_rank": coin.get("market_cap_rank"),
                    "price_btc": coin.get("price_btc"),
                }
            )

        df = pd.DataFrame(cleaned_list)
        df.dropna(inplace=True)
        df.to_csv("cleaned_data.csv", index=False)
        print("Data cleaned and saved to cleaned_data.csv")
    except Exception as e:
        print(f"Error cleaning data: {e}")


if __name__ == "__main__":
    clean_data()