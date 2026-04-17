from datetime import date
from pathlib import Path

today = date.today()
today_iso = today.isoformat()

# Folder name: e.g. "2026"
year_folder_name = today.strftime("%Y")

# File name: e.g. "January.md"
month_file_name = f"{today.strftime('%m-%B')}.md"

base_dir = Path("/home/dan/Documents/Notes/Pitbull Catch-Ups")
year_dir = base_dir / year_folder_name

# Create the yearly folder if it doesn't exist
year_dir.mkdir(parents=True, exist_ok=True)

# Markdown content
markdown_content = f"""
### {today_iso}

**Dan**
 * No updates

**James**
 * No updates

**Callie**
 * No updates

"""

# File path inside the yearly folder
file_path = year_dir / month_file_name

# Append the content
with open(file_path, "a", encoding="utf-8") as f:
    f.write(markdown_content.strip() + "\n\n")
