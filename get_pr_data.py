import requests
import datetime
import sys
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API_URL = "https://api.github.com/search/issues"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_last_week_date():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    return last_week.strftime("%Y-%m-%d")


def search_merged_prs(username, date_range=None):
    """Search for merged PRs by a specific GitHub user in the last week."""
    if not date_range:
        date_range = get_last_week_date()

    query = f"type:pr is:merged author:{username} merged:>={date_range}"

    params = {"q": query, "sort": "updated", "order": "desc", "per_page": 100}

    headers = {"Accept": "application/vnd.github+json"}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    else:
        print("Warning: No GITHUB_TOKEN found")

    response = requests.get(GITHUB_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

    data = response.json()
    return data.get("items", [])


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_pr_data.py <github_username>")
        sys.exit(1)

    username = sys.argv[1]
    prs = search_merged_prs(username)

    print(f"\nMerged PRs by {username} in the last week:\n")
    if not prs:
        print("No merged PRs found.")
        return

    for pr in prs:
        title = pr["title"]
        url = pr["html_url"]
        repo = pr["repository_url"].split("/")[-1]
        merged_at = pr["closed_at"].split("T")[0]
        print(f"- [{title}]({url}) in {repo} (merged on {merged_at})")


if __name__ == "__main__":
    main()
