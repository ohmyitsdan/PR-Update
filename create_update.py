import datetime
import os
import json
from get_pr_data import search_merged_prs

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
            prs = search_merged_prs(username)

            f.write(f"## {name}\n\n")

            if not prs:
                f.write("No merged PRs in the last week.\n\n")
                continue

            for pr in prs:
                title = pr["title"]
                url = pr["html_url"]
                repo = pr["repository_url"].split("/")[-1]
                merged_at = pr["closed_at"].split("T")[0]
                f.write(f"- [{title}]({url}) in `{repo}` (merged on {merged_at})\n")
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
