# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:04:19 2025

@author: fabijans-1
"""

import os
import pandas as pd

def rename_columns_in_excel_files(folder_path):
    # Go through all the files in the folder and subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            if ('contacts' in file) and file.endswith('.xlsx') or file.endswith('.xls'):
                # Type the contacts or customers above in order to choose which type of reports you want to select
                file_path = os.path.join(root, file)
                try:
                    # Load an Excel file
                    df = pd.read_excel(file_path)
                    
                    # CHeck existing columns
                    print(f'Kolumny w pliku {file_path}: {df.columns.tolist()}')

                    # Dictionary with names to change
                    columns_to_rename = {
                        'old_column_1': 'new_column_1',
                        'old_column_2': 'new_column_2',
                        'old_column_3': 'new_column_3',
                        'old_column_4': 'new_column_4',
                    }

                    # Check which columns exist and rename them
                    existing_columns = {col: columns_to_rename[col] for col in columns_to_rename if col in df.columns}
                    print(f'Istniejące kolumny do zmiany w pliku {file_path}: {existing_columns}')
                    if existing_columns:
                        df.rename(columns=existing_columns, inplace=True)
                        # Save modified file
                        df.to_excel(file_path, index=False)
                        print(f'Columns changed in file: {file_path}')
                except Exception as e:
                    print(f'Error while processing the file {file_path}: {e}')

# Folder path
folder_path = r"folderpath"
rename_columns_in_excel_files(folder_path)
