# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:12:06 2025

@author: fabijans-1
"""

import pandas as pd
import os
from collections import Counter

def count_columns_in_excel_files(folder_path):
    column_counter = Counter()

    # Traversing through all files in the folder and subfolders.
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if ('contacts' in file) and file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                try:
                    # Reading an Excel file.
                    df = pd.read_excel(file_path)
                    # Counting columns.
                    column_counter.update(df.columns)
                except Exception as e:
                    print(f'Nie można odczytać pliku {file_path}: {e}')

    # Displaying results.
    for column, count in column_counter.items():
        print(f"{column} - ilość: {count}")

# Set the path to the folder with Excel files.
folder_path = r"folderpathwithfiles"
count_columns_in_excel_files(folder_path)
