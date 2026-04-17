from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/danbicker/Documents/Docs/Docs/Pitbull Catch-Ups")

MONTHS = {datetime(2000, m, 1).strftime("%B"): f"{m:02d}" for m in range(1, 13)}


def rename_month_files(base_dir: Path) -> None:
    for year_dir in base_dir.iterdir():
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue

        for file in year_dir.iterdir():
            if file.suffix != ".md":
                continue

            month_name = file.stem
            if month_name not in MONTHS:
                continue  # already renamed or non-month file

            new_name = f"{MONTHS[month_name]}-{month_name}.md"
            new_path = file.with_name(new_name)

            if new_path.exists():
                print(f"⚠️  Skipping (exists): {new_path}")
                continue

            file.rename(new_path)
            print(f"✔ Renamed: {file.name} → {new_name}")


rename_month_files(
    Path("/home/danbicker/Documents/Docs/Docs/Pitbull Catch-Ups")
)
