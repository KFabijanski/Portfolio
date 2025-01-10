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

    # Przechodzenie przez wszystkie pliki w folderze i podfolderach
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if ('contacts' in file) and file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                try:
                    # Odczyt pliku Excel
                    df = pd.read_excel(file_path)
                    # Zliczanie kolumn
                    column_counter.update(df.columns)
                except Exception as e:
                    print(f'Nie można odczytać pliku {file_path}: {e}')

    # Wyświetlanie wyników
    for column, count in column_counter.items():
        print(f"{column} - ilość: {count}")

# Ustaw ścieżkę do folderu z plikami Excel
folder_path = r"C:\Users\fabijans-1\OneDrive - Mettler Toledo LLC\All units task list\Data Quality\Weekly checks\Archive"
count_columns_in_excel_files(folder_path)