# Excel Data Quality Comparison Tool

## Overview

This script is designed to compare two Excel files and detect row-level differences across all sheets. It is mainly used for data quality validation and reconciliation between reporting datasets.

The tool handles real-world data inconsistencies such as:

* different date formats
* inconsistent text formatting
* duplicate rows
* technical metadata rows from exports

---

## How to run the script

### 1. Setup

Download the script and place it in a working directory.

Add the two Excel files you want to compare into the same folder.

### 2. Run the script

Open terminal in the folder and execute:

```bash
python Excel_compare_script.py [file1].xlsx [file2].xlsx
```

Replace:

* `[file1]` – first Excel file
* `[file2]` – second Excel file

---

## Output example

If differences exist, the script will return output like:

```
Differences found:
Coupon - overview - row only in file 1: 2026-05-18 - 2026-05-24 | empty cell | 4251055
Coupon - overview - row only in file 2: 2026-05-18 - 2026-05-24 | 2581955 | 4251055 
```

If no differences are found:

```
No differences found.
```

---

## Debug version

There is also a debug version:
`Excel_compare_debug.py`

This version performs deeper analysis to help identify potential root causes of inconsistencies.

⚠️ Note:
It is more computationally expensive and should only be used when standard comparison is not sufficient.

---

## Notes

* The script may generate openpyxl warnings related to workbook styling — these do not affect functionality.
* Designed for internal data validation workflows.
