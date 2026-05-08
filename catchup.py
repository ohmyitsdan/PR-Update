import json
import os
from datetime import date
from pathlib import Path

today = date.today()
today_iso = today.isoformat()

# Folder name: e.g. "2026"
year_folder_name = today.strftime("%Y")

# File name: e.g. "January.md"
month_file_name = f"{today.strftime('%m-%B')}.md"

base_dir = Path(os.getenv("CATCHUP_DIR"))
year_dir = base_dir / year_folder_name

# Create the yearly folder if it doesn't exist
year_dir.mkdir(parents=True, exist_ok=True)


# Load teammate names from users.json

users_path = Path(__file__).parent / "users.json"
with open(users_path, "r", encoding="utf-8") as f:
    users = json.load(f)

markdown_content = f"### {today_iso}\n\n"
for name in users.keys():
    markdown_content += f"**{name}**\n * No updates\n\n"

# File path inside the yearly folder
file_path = year_dir / month_file_name

# Append the content
with open(file_path, "a", encoding="utf-8") as f:
    f.write(markdown_content.strip() + "\n\n")
