# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:04:19 2025

@author: fabijans-1
"""

import os
import pandas as pd

def rename_columns_in_excel_files(folder_path):
    # Przechodzimy przez wszystkie pliki w folderze i podfolderach
    for root, _, files in os.walk(folder_path):
        for file in files:
            if ('contacts' in file) and file.endswith('.xlsx') or file.endswith('.xls'):
                file_path = os.path.join(root, file)
                try:
                    # Odczytujemy plik Excel
                    df = pd.read_excel(file_path)
                    
                    # Sprawdź istniejące kolumny
                    print(f'Kolumny w pliku {file_path}: {df.columns.tolist()}')

                    # Definiujemy słownik z kolumnami do zmiany
                    columns_to_rename = {
                        'Customer - ID.1': 'Customer name',
                    }

                    # Sprawdzamy, które kolumny istnieją i zmieniamy ich nazwy
                    existing_columns = {col: columns_to_rename[col] for col in columns_to_rename if col in df.columns}
                    print(f'Istniejące kolumny do zmiany w pliku {file_path}: {existing_columns}')
                    if existing_columns:
                        df.rename(columns=existing_columns, inplace=True)
                        # Zapisujemy zmodyfikowany plik
                        df.to_excel(file_path, index=False)
                        print(f'Zmieniono kolumny w pliku: {file_path}')
                except Exception as e:
                    print(f'Błąd przy przetwarzaniu pliku {file_path}: {e}')

# Podaj ścieżkę do folderu
folder_path = r"C:\Users\fabijans-1\OneDrive - Mettler Toledo LLC\All units task list\Data Quality\Weekly checks\Archive"
rename_columns_in_excel_files(folder_path)
