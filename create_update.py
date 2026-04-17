import datetime
import os
import json
from get_pr_data import search_prs

from dotenv import load_dotenv

load_dotenv()


def create_update(users, output_dir):
    """Create a markdown file with merged PRs for each user."""
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    filename = f"{today_str}.md"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, "w") as f:
        title = os.getenv("TITLE")
        f.write(f"# {title}\n\n")

        for name, username in users.items():
            merged_prs = search_prs(username, pr_type="merged", repo="Beauhurst/UKF")
            today = datetime.datetime.now(datetime.timezone.utc)
            last_month = today - datetime.timedelta(days=30)
            open_prs = search_prs(username, pr_type="open", date_range=last_month, repo="Beauhurst/UKF")
            f.write(f"### {name}\n\n")

            if not any([merged_prs, open_prs]):
                f.write("No PRs in the last week.\n\n")
                continue

            f.write("##### Merged\n\n")

            if not merged_prs:
                f.write("No merged PRs in the last week.\n\n")
            else:
                for pr in merged_prs:
                    title = pr["title"]
                    url = pr["html_url"]
                    merged_at = pr["closed_at"].split("T")[0]
                    f.write(f"- {title} - {url} (merged on {merged_at})\n")
                f.write("\n")

            f.write("##### Open\n\n")

            if not open_prs:
                f.write("No open PRs in the last week.\n\n")
            else:
                for pr in open_prs:
                    title = pr["title"]
                    url = pr["html_url"]
                    f.write(f"- {title} - {url}\n")
                f.write("\n")

    print(f"Created update file: {filepath}")


def load_users(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    users = load_users("users.json")

    output_directory = os.getenv("OUTPUT_DIR")

    create_update(users, output_directory)
