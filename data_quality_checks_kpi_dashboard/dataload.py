# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:32:50 2025

@author: fabijans-1
"""

import os
import pandas as pd

# Ustawienia
folder_path = r"C:\Users\fabijans-1\OneDrive - Mettler Toledo LLC\All units task list\Data Quality\Weekly checks\Archive"
customers_output_file = "combined_customers.xlsx"  # Nowy plik Excel dla customers
contacts_output_file = "combined_contacts.xlsx"  # Nowy plik Excel dla contacts

# Mapowanie kolumn
customers_column_mapping = {
    'Sales Organization': 'salesorg',
    'Account ID': 'accountid',
    'Account Site ID': 'accountsiteid',
    'Holding': 'holding',
    'Name 1': 'name1',
    'Name 2': 'name2',
    'Name 3': 'name3',
    'Country': 'country',
    'City': 'city',
    'Postal Code': 'postalcode',
    'Street': 'street1',
    'Street 2': 'street2',
    'Created On': 'createdon',
    'Created By': 'createdby',
    'Account Role Description': 'bprole',
    'Type': 'type',
    'Status': 'stat',
    'Comment': 'comment',
}

contacts_column_mapping = {
    'Customer - ID': 'accountid',
    'Contact Person - ID': 'contactid',
    'Contact Person - E-Mail Address': 'email',
    'Contact Person - First Name': 'firstname',
    'Contact Person - Surname': 'lastname',
    'Country': 'country',
    'Account Role Description': 'bprole',
    'Contact Person - Creation Date': 'createdon',
    'Contact Person - Created by': 'createdby',
    'Account Role Description': 'bprole',
    'Type': 'type',
    'Status': 'stat',
    'Comments': 'comment',
}


# Funkcja do przetwarzania pliku Excel
def process_file(file_path, column_mapping):
    df = pd.read_excel(file_path)
    filtered_columns = [col for col in column_mapping.keys() if col in df.columns]
    df_filtered = df[filtered_columns].rename(columns=column_mapping)  # Zmiana nazw kolumn na podstawie mapowania
    df_filtered['filename'] = file_path  # Dodanie nowej kolumny z nazwą pliku
    df_filtered['createdon'] = pd.to_datetime(df_filtered['createdon'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
    return df_filtered

# Funkcja do przeszukiwania folderów
def search_files(folder):
    customers_data = pd.DataFrame()  # DataFrame do kondensowania danych z customers
    contacts_data = pd.DataFrame()    # DataFrame do kondensowania danych z contacts

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Ignoruj pliki wynikowe
            if file_path in (os.path.join(folder_path, customers_output_file), os.path.join(folder_path, contacts_output_file)):
                continue
            
            if 'customers' in file and file.endswith('.xlsx'):
                print(f'Przetwarzanie pliku customers: {file_path}')
                df = process_file(file_path, customers_column_mapping)
                customers_data = pd.concat([customers_data, df], ignore_index=True)
            elif 'contacts' in file and file.endswith('.xlsx'):
                print(f'Przetwarzanie pliku contacts: {file_path}')
                df = process_file(file_path, contacts_column_mapping)
                contacts_data = pd.concat([contacts_data, df], ignore_index=True)

    # Zapisz skondensowane dane do nowych plików Excel
    customers_data.to_excel(os.path.join(folder_path, customers_output_file), index=False)
    print(f'Skondensowane dane customers zapisano w pliku: {os.path.join(folder_path, customers_output_file)}')
    
    contacts_data.to_excel(os.path.join(folder_path, contacts_output_file), index=False)
    print(f'Skondensowane dane contacts zapisano w pliku: {os.path.join(folder_path, contacts_output_file)}')

# Rozpocznij przeszukiwanie folderu
search_files(folder_path)




