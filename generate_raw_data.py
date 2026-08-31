import os
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import re
import shutil


BASE_DIR = Path.home() / 'Desktop' / 'raw data'


def generate_random_files(count: int = 50) -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    companies = [
        'acme', 'northstar', 'bluebird', 'summit', 'harbor', 'peak', 'lumen', 'atlas', 'solstice', 'cobalt',
        'evergreen', 'meridian', 'horizon', 'amber', 'cascade', 'pinecrest', 'silverline', 'brookstone', 'redwood', 'mariner',
        'vanguard', 'frontier', 'spectrum', 'opal', 'granite', 'signal', 'nexa', 'quartz', 'everest', 'wildflower',
        'sunset', 'brisk', 'terra', 'mosaic', 'cinder', 'swift', 'relay', 'stellar', 'saffron', 'willow',
        'drift', 'apex', 'harvest', 'voyager', 'bramble', 'hollow', 'ion', 'monarch', 'arcadia', 'pioneer'
    ]

    start = datetime(2023, 1, 1)
    for i in range(count):
        company = random.choice(companies)
        offset = random.randint(0, 1100)
        date = start + timedelta(days=offset)
        file_name = f"{company}_{date.strftime('%Y%m%d')}.txt"
        file_path = BASE_DIR / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"sample_id: {i + 1}\n")
            f.write(f"company: {company}\n")
            f.write(f"date: {date.strftime('%Y-%m-%d')}\n")
            f.write(f"payload: {''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(60))}\n")
            f.write("status: random_generated\n")

    print(f"Created {count} random files in {BASE_DIR}")


def organize_by_year_month_day() -> None:
    if not BASE_DIR.exists():
        raise FileNotFoundError(f"Folder does not exist: {BASE_DIR}")

    pattern = re.compile(r'^(?P<company>.+)_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.txt$')
    moved = 0

    for item in sorted(BASE_DIR.iterdir()):
        if not item.is_file() or item.suffix.lower() != '.txt':
            continue

        match = pattern.match(item.name)
        if not match:
            continue

        year = match.group('year')
        month = match.group('month')
        day = match.group('day')

        target_dir = BASE_DIR / year / month / day
        target_dir.mkdir(parents=True, exist_ok=True)

        dest = target_dir / item.name
        if dest.exists():
            stem = item.stem
            counter = 1
            while dest.exists():
                dest = target_dir / f"{stem}_{counter}.txt"
                counter += 1

        shutil.move(str(item), str(dest))
        moved += 1

    print(f"Moved {moved} txt files into year/month/day folders under {BASE_DIR}")


if __name__ == '__main__':
    generate_random_files(50)
    organize_by_year_month_day()
