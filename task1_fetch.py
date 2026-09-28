import json
import urllib.request


def fetch_trending_data():
    url = "https://api.coingecko.com/api/v3/search/trending"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("Data fetched successfully!")

            with open("raw_data.json", "w") as f:
                json.dump(data, f, indent=4)
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


if __name__ == "__main__":
    fetch_trending_data()