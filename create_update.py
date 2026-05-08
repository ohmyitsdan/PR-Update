import datetime
import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from get_pr_data import get_pr_details, search_prs

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

SUMMARY_PROMPT_FILE_NAME = "summary_prompt.txt"
SUMMARY_PROMPT_PATH = os.path.join(SCRIPT_DIR, SUMMARY_PROMPT_FILE_NAME)

client = Anthropic()


def generate_summary(pr_data: dict) -> str:
    """Generate an AI summary of the week's PR activity."""
    lines = []
    for name, data in pr_data.items():
        merged = data["merged"]
        open_ = data["open"]
        if merged:
            entries = ", ".join(f"{pr['title']} ({pr['html_url']})" for pr in merged)
            lines.append(f"{name} merged: {entries}")
        if open_:
            entries = ", ".join(f"{pr['title']} ({pr['html_url']})" for pr in open_)
            lines.append(f"{name} has open PRs: {entries}")

    if not lines:
        return "_No PR activity to summarise._\n\n"

    with open(SUMMARY_PROMPT_PATH) as f:
        prompt_template = f.read()

    pr_text = "\n".join(lines)
    prompt = prompt_template.format(pr_text=pr_text)

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip() + "\n\n"


def create_update(users, output_dir):
    """Create a markdown file with merged PRs for each user."""
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    filename = f"{today_str}.md"
    filepath = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.datetime.now(datetime.timezone.utc)
    last_month = today - datetime.timedelta(days=30)

    # Fetch all PR data up front so we can pass it to the summariser
    pr_data = {}
    owner = os.getenv("OWNER")
    repo = os.getenv("REPO")
    repo_full = f"{owner}/{repo}"
    for name, username in users.items():
        pr_data[name] = {
            "merged": [
                get_pr_details(pr)
                for pr in search_prs(username, pr_type="merged", repo=repo_full)
            ],
            "open": [
                get_pr_details(pr)
                for pr in search_prs(
                    username,
                    pr_type="open",
                    date_range=last_month,
                    repo=repo_full,
                )
            ],
        }

    with open(filepath, "w") as f:
        title = os.getenv("TITLE")
        f.write(f"# {title}\n\n")

        f.write("## Summary\n\n")
        f.write(generate_summary(pr_data))

        for name, data in pr_data.items():
            merged_prs = data["merged"]
            open_prs = data["open"]

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
