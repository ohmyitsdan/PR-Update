from datetime import datetime
from pathlib import Path
import re


def migrate_sections_to_year_month_files(
    source_file: Path,
    base_dir: Path,
) -> None:
    """
    Move dated markdown sections into year/month files.

    - Year folders: YYYY/
    - Files: Month.md (e.g. June.md)
    - Sections must start with '## YYYY-MM-DD' or '### YYYY-MM-DD'
    """

    content = source_file.read_text(encoding="utf-8")

    # Match headers like:
    # ## 2025-06-12
    # ### 2025-06-12
    section_regex = re.compile(
        r"(#{2,3}\s+\d{4}-\d{2}-\d{2}.*?)(?=\n#{2,3}\s+\d{4}-\d{2}-\d{2}|\Z)",
        re.S,
    )

    sections = section_regex.findall(content)

    for section in sections:
        # Extract the date
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", section)
        if not date_match:
            continue

        section_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")

        year_dir = base_dir / section_date.strftime("%Y")
        year_dir.mkdir(parents=True, exist_ok=True)

        month_file = year_dir / f"{section_date.strftime('%B')}.md"

        with open(month_file, "a", encoding="utf-8") as f:
            f.write(section.strip() + "\n\n")


if __name__ == "__main__":
    migrate_sections_to_year_month_files(
        source_file=Path("/home/danbicker/Documents/Docs/Docs/Pitbull Weekly Updates/Pitbull Catch-Ups.md"),
        base_dir=Path("/home/danbicker/Documents/Docs/Docs/Pitbull Weekly Updates"),
    )
