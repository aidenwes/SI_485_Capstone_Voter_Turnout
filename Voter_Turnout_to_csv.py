import csv
import re
import os
from pathlib import Path
import chardet


def detect_encoding(path, sample_size=4096):
    """Detect file encoding using a small sample (uses chardet if available)."""
    try:
        with open(path, 'rb') as f:
            raw = f.read(sample_size)
        result = chardet.detect(raw)
        return result['encoding'] or 'utf-8'
    except Exception:
        return 'utf-8'


def parse_lines(lines):
    """Parse lines into rows using tabs or multiple spaces as separators.

    Returns list of lists (columns). Skips empty and obvious header/footer lines.
    """
    rows = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip common header/footer markers
        if line.startswith('County Code') or line.startswith('RECORDS:'):
            continue

        parts = re.split(r'\t+|\s{2,}', line)
        if len(parts) >= 3:
            # Normalize county name spacing like original script
            parts[1] = parts[1].replace(' COUNTY', '_COUNTY')
            rows.append(parts[:3])
    return rows


def convert_txt_to_csv(txt_path: Path, keep_original=True):
    """Convert a single txt file to csv. Returns number of rows written.

    The CSV is written next to the .txt file with the same stem.
    """
    enc = detect_encoding(txt_path)
    with open(txt_path, 'r', encoding=enc, errors='replace') as f:
        lines = f.readlines()

    rows = parse_lines(lines)
    if not rows:
        return 0

    csv_path = txt_path.with_suffix('.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['County_Code', 'County_Name', 'County_Voters'])
        writer.writerows(rows)

    return len(rows)


def main():
    base_dir = Path(__file__).parent
    voter_dir = base_dir / 'Voter_Turnout_Data'
    if not voter_dir.exists():
        print(f"Directory not found: {voter_dir}")
        return

    txt_files = list(voter_dir.glob('*.txt'))
    if not txt_files:
        print(f"No .txt files found in {voter_dir}")
        return

    summary = []
    for txt in txt_files:
        try:
            count = convert_txt_to_csv(txt)
            summary.append((txt.name, count))
            print(f"Converted {txt.name} -> {txt.with_suffix('.csv').name} ({count} rows)")
        except Exception as e:
            print(f"Failed to convert {txt.name}: {e}")

    total = sum(c for _, c in summary)
    print('---')
    print(f"Processed {len(summary)} files. Total rows: {total}")


if __name__ == '__main__':
    main()