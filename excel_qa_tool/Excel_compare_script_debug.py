from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime, date
import sys
import re


EXCLUDED_ROW_PREFIXES = (
    "Data extract produced by",
)

# Ustaw to jawnie jeśli slashowe daty są w formacie:
# "mdy" -> 03/01/2025 = Mar 1, 2025
# "dmy" -> 03/01/2025 = 3 Jan 2025
SLASH_DATE_ORDER = "mdy"


def normalize_date_token(token):
    token = token.strip()

    if "/" in token:
        if SLASH_DATE_ORDER == "mdy":
            formats = ["%m/%d/%Y", "%d/%m/%Y"]
        else:
            formats = ["%d/%m/%Y", "%m/%d/%Y"]
    elif "." in token:
        formats = ["%d.%m.%Y"]
    elif "-" in token:
        formats = ["%Y-%m-%d", "%d-%m-%Y"]
    else:
        formats = []

    for fmt in formats:
        try:
            dt = datetime.strptime(token, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return token


def normalize_text(value):
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    value = value.casefold()

    value = re.sub(r"\b\d{2}\.\d{2}\.\d{4}\b",
                   lambda m: normalize_date_token(m.group(0)), value)
    value = re.sub(r"\b\d{2}/\d{2}/\d{4}\b",
                   lambda m: normalize_date_token(m.group(0)), value)
    value = re.sub(r"\b\d{4}-\d{2}-\d{2}\b",
                   lambda m: normalize_date_token(m.group(0)), value)
    value = re.sub(r"\b\d{2}-\d{2}-\d{4}\b",
                   lambda m: normalize_date_token(m.group(0)), value)

    return value


def normalize_value(value):
    """
    Normalization for comparison.
    Preserves the meaning of numbers but removes noise like 115.0 vs 115.
    Also normalizes date/datetime values and date-like strings.
    """
    if value is None:
        return ""

    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    if isinstance(value, str):
        val = normalize_text(value)

        # Attempt to convert plain numeric strings
        try:
            num = float(val)
            if num.is_integer():
                return int(num)
            return num
        except ValueError:
            return val

    return value


def visible_value(value):
    """
    Shows invisible characters in a readable way.
    """
    if value is None:
        return "<None>"
    if isinstance(value, str):
        return value.replace(" ", "·").replace("\xa0", "⍽")
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    return str(value)


def cell_repr(value):
    return f"{visible_value(value)} ({type(value).__name__})"


def is_ignored_row(normalized_row):
    """
    Skips empty and technical rows in the export.
    """
    non_empty = [v for v in normalized_row if v != ""]
    if not non_empty:
        return True

    first = str(non_empty[0]).strip()
    for prefix in EXCLUDED_ROW_PREFIXES:
        if first.startswith(prefix):
            return True

    return False


def row_signature(row_values):
    return tuple(normalize_value(v) for v in row_values)


def row_text(row_values):
    return " | ".join(cell_repr(v) for v in row_values)


def collect_rows(ws):
    rows = []
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
        raw_values = list(row)
        normalized = [normalize_value(v) for v in raw_values]

        if is_ignored_row(normalized):
            continue

        rows.append({
            "row_num": row_idx,
            "raw": raw_values,
            "norm": tuple(normalized),
        })
    return rows


def similarity(row_a, row_b):
    a = " || ".join(map(str, row_a["norm"]))
    b = " || ".join(map(str, row_b["norm"]))
    return SequenceMatcher(None, a, b).ratio()


def best_match(target_row, candidate_rows):
    if not candidate_rows:
        return None, 0.0

    best = None
    best_score = -1.0
    for cand in candidate_rows:
        score = similarity(target_row, cand)
        if score > best_score:
            best_score = score
            best = cand
    return best, best_score


def compare_two_rows(row1, row2):
    """
    Returns cell-by-cell differences for two rows.
    """
    max_len = max(len(row1["raw"]), len(row2["raw"]))
    diffs = []

    for idx in range(max_len):
        v1 = row1["raw"][idx] if idx < len(row1["raw"]) else None
        v2 = row2["raw"][idx] if idx < len(row2["raw"]) else None

        n1 = normalize_value(v1)
        n2 = normalize_value(v2)

        if n1 != n2:
            col = get_column_letter(idx + 1)
            diffs.append(f"    {col}: file1={cell_repr(v1)} | file2={cell_repr(v2)}")

    return diffs


def compare_excels(file1, file2, sheet_filter=None):
    wb1 = load_workbook(file1, data_only=True)
    wb2 = load_workbook(file2, data_only=True)

    sheets1 = set(wb1.sheetnames)
    sheets2 = set(wb2.sheetnames)

    common_sheets = sorted(sheets1 & sheets2)

    if sheet_filter:
        common_sheets = [s for s in common_sheets if s == sheet_filter]

    report = []

    for sheet_name in common_sheets:
        ws1 = wb1[sheet_name]
        ws2 = wb2[sheet_name]

        rows1 = collect_rows(ws1)
        rows2 = collect_rows(ws2)

        c1 = Counter(r["norm"] for r in rows1)
        c2 = Counter(r["norm"] for r in rows2)

        only1 = c1 - c2
        only2 = c2 - c1

        if not only1 and not only2:
            report.append(f"[{sheet_name}] no differences after normalization.")
            continue

        report.append(f"\n[{sheet_name}] differences found after normalization.")
        report.append(f"  file1 rows: {len(rows1)}")
        report.append(f"  file2 rows: {len(rows2)}")

        if only1:
            report.append("  Rows only in file1:")
            for signature, count in only1.items():
                sample1 = next(r for r in rows1 if r["norm"] == signature)
                candidates = [r for r in rows2 if len(r["raw"]) == len(sample1["raw"])]
                best, score = best_match(sample1, candidates)

                report.append(f"    - count={count}")
                report.append(f"      file1 row {sample1['row_num']}: {row_text(sample1['raw'])}")

                if best is not None:
                    report.append(
                        f"      best match in file2 row {best['row_num']} "
                        f"(similarity={score:.3f}): {row_text(best['raw'])}"
                    )
                    cell_diffs = compare_two_rows(sample1, best)
                    if cell_diffs:
                        report.append("      cell differences:")
                        report.extend(cell_diffs)
                else:
                    report.append("      no meaningful match in file2")

        if only2:
            report.append("  Rows only in file2:")
            for signature, count in only2.items():
                sample2 = next(r for r in rows2 if r["norm"] == signature)
                candidates = [r for r in rows1 if len(r["raw"]) == len(sample2["raw"])]
                best, score = best_match(sample2, candidates)

                report.append(f"    - count={count}")
                report.append(f"      file2 row {sample2['row_num']}: {row_text(sample2['raw'])}")

                if best is not None:
                    report.append(
                        f"      best match in file1 row {best['row_num']} "
                        f"(similarity={score:.3f}): {row_text(best['raw'])}"
                    )
                    cell_diffs = compare_two_rows(best, sample2)
                    if cell_diffs:
                        report.append("      cell differences:")
                        report.extend(cell_diffs)
                else:
                    report.append("      no meaningful match in file1")

    return report


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print("Usage: python compare_excels.py file1.xlsx file2.xlsx [sheet_name]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) == 4 else None

    differences = compare_excels(file1, file2, sheet_name)

    if not differences:
        print("No differences found.")
    else:
        print("Differences found:")
        for line in differences:
            print(line)