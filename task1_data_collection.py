from datetime import datetime
import json
import os
import time
import requests

# 1. Categories & Keyword mapping
CATEGORIES = {
    "technology": [
        "ai",
        "software",
        "tech",
        "code",
        "computer",
        "data",
        "cloud",
        "api",
        "gpu",
        "llm",
    ],
    "worldnews": [
        "war",
        "government",
        "country",
        "president",
        "election",
        "climate",
        "attack",
        "global",
    ],
    "sports": [
        "nfl",
        "nba",
        "fifa",
        "sport",
        "game",
        "team",
        "player",
        "league",
        "championship",
    ],
    "science": [
        "research",
        "study",
        "space",
        "physics",
        "biology",
        "discovery",
        "nasa",
        "genome",
    ],
    "entertainment": [
        "movie",
        "film",
        "music",
        "netflix",
        "game",
        "book",
        "show",
        "award",
        "streaming",
    ],
}


def categorize_story(title):
    # Categorize story based on keywords in title
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in title_lower:
                return category
    return "other"


def fetch_hacker_news_trends():
    headers = {"User-Agent": "TrendPulse/1.0"}
    top_stories_url = (
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    )

    try:
        # Fetch top story IDs
        response = requests.get(top_stories_url, headers=headers)
        story_ids = response.json()[:500]  # Fetch first 500 IDs
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    collected_stories = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}

    for story_id in story_ids:
        # Stop if we collected 25 stories for each category
        if all(count >= 25 for count in category_counts.values()):
            break

        story_url = (
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        try:
            res = requests.get(story_url, headers=headers)
            story = res.json()

            if not story or story.get("type") != "story":
                continue

            title = story.get("title", "")
            category = categorize_story(title)

            # Skip if category is full or not in our target list
            if category == "other" or category_counts[category] >= 25:
                continue

            # Extract required fields
            story_data = {
                "post_id": story.get("id"),
                "title": title,
                "url": story.get("url", ""),
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": category,
            }

            collected_stories.append(story_data)
            category_counts[category] += 1
            time.sleep(0.05)  # Small delay between requests

        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            continue

    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save to JSON file with format trends_YYYYMMDD.json
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w") as f:
        json.dump(collected_stories, f, indent=4)

    print(
        f"Collected {len(collected_stories)} stories. Saved to {file_path}"
    )


if __name__ == "__main__":
    fetch_hacker_news_trends()