import os
import requests
import json
from datetime import datetime

def fetch_hacker_news_trends():
    os.makedirs("data", exist_ok=True)
    
    # Fetch top story IDs from Hacker News API
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    
    if response.status_code != 200:
        print("Error fetching top stories")
        return

    story_ids = response.json()[:50]  # Fetch top 50 stories
    collected_stories = []

    print("Fetching stories data...")
    for story_id in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item_resp = requests.get(item_url)
        if item_resp.status_code == 200:
            story_data = item_resp.json()
            if story_data and story_data.get("type") == "story":
                collected_stories.append({
                    "id": story_data.get("id"),
                    "title": story_data.get("title"),
                    "score": story_data.get("score", 0),
                    "by": story_data.get("by"),
                    "time": story_data.get("time"),
                    "comments_count": story_data.get("descendants", 0),
                    "url": story_data.get("url", "")
                })

    # Save to JSON file with format trends_YYYYMMDD.json
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"Collected {len(collected_stories)} stories. Saved to {file_path}")

if __name__ == "__main__":
    fetch_hacker_news_trends()