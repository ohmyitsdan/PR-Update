import requests
import datetime
import sys
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API_URL = "https://api.github.com/search/issues"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_last_week_date():
    today = datetime.datetime.now(datetime.timezone.utc)
    last_week = today - datetime.timedelta(days=5)
    return last_week


def search_prs(username, pr_type="merged", date_range=None, repo=None):
    """Search for merged PRs by a specific GitHub user in the last week."""
    if not date_range:
        date_range = get_last_week_date()

    print(f"Checking for {pr_type} PRs for {username} since {date_range.strftime('%d-%b')}")

    if type(date_range) != str:
        date_range = date_range.strftime('%Y-%m-%d')

    query = f"is:pr author:{username}"

    if pr_type == "merged":
        query += f" is:merged merged:>={date_range}"
    else:
        query += " is:open"

    if repo:
        query += f" repo:{repo}"

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
    total_count = data.get("total_count", 0)
    return data.get("items", [])


def print_prs(prs, heading):
    """Helper to print PR list nicely."""
    print(f"\n{heading}:\n")
    if not prs:
        print("None found.")
        return

    for pr in prs:
        title = pr["title"]
        url = pr["html_url"]
        repo = pr["repository_url"].split("/")[-1]
        date_field = "closed_at" if pr.get("closed_at") else "created_at"
        date_value = pr[date_field].split("T")[0]
        status = "merged" if pr.get("closed_at") else "opened"
        print(f"- [{title}]({url}) in {repo} ({status} on {date_value})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_pr_data.py <github_username> [--count-only]")
        sys.exit(1)
    
    username = sys.argv[1]
    count_only = "--count-only" in sys.argv
    
    merged_prs = search_prs(username, pr_type="merged")
    open_prs = search_prs(username, pr_type="open")
    
    if count_only:
        print(f"Merged: {len(merged_prs)}")
        print(f"Open: {len(open_prs)}")
        print(f"Total: {len(merged_prs) + len(open_prs)}")
    else:
        print(f"\nTotal merged PRs: {len(merged_prs)}")
        print(f"Total open PRs: {len(open_prs)}")
        print_prs(merged_prs, f"Merged PRs by {username} in the last week")
        print_prs(open_prs, f"Open PRs by {username}")

if __name__ == "__main__":
    main()
