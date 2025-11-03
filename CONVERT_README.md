`fixthetxt.py` converts all `.txt` files in the `Voter_Turnout_Data/` folder into `.csv` files while preserving the original `.txt` files.

Usage

1. Ensure you have Python 3.8+ installed.
2. Run the converter from the project root:

   python fixthetxt.py

This will create `.csv` files next to each `.txt` in `Voter_Turnout_Data/`.

Notes

- The script attempts to detect file encodings using `chardet` and writes CSVs with UTF-8 encoding.
- It parses columns separated by tabs or multiple spaces and writes the first three columns as `County_Code,County_Name,County_Voters`.
