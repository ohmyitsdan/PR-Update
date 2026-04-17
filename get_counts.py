import requests
from collections import Counter
from dotenv import load_dotenv
import os

# --- Configuration ---
OWNER = "Beauhurst"
REPO = "ukf"
BRANCH = "customisable-dashboard"


load_dotenv()

GITHUB_API_URL = "https://api.github.com/search/issues"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- GitHub API Setup ---
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

commit_counts = Counter()
page = 1

print("Getting commits")
while True:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"
    params = {"sha": BRANCH, "per_page": 100, "page": page}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data or "message" in data:
        break  # No more commits or error

    for commit in data:
        # Prefer GitHub username if available
        if commit.get("author") and commit["author"].get("login"):
            name = commit["author"]["login"]
        else:
            name = commit["commit"]["author"]["name"]
        commit_counts[name] += 1

    print("PAGE", page)
    page += 1
    if page >= 2:
        break


# --- Results ---
for author, count in commit_counts.most_common():
    print(f"{author}: {count} commits")
