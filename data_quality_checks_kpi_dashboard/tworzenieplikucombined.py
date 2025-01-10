import os
import pandas as pd

# Combined Contacts  
# Ustawienie ścieżki do folderu z plikami Excel
folder_path = r"C:\Users\fabijans-1\OneDrive - Mettler Toledo LLC\All units task list\Data Quality\Weekly checks\Archive"  # Zmień tę ścieżkę

# Lista do przechowywania DataFrame'ów
dataframes = []

# Iteracja przez pliki w folderze i podfolderach
for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.endswith('.xlsx') and 'contacts' in filename:
            file_path = os.path.join(dirpath, filename)
            
            # Wczytaj plik Excel
            try:
                df = pd.read_excel(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Nie udało się wczytać pliku {filename}: {e}")

# Skondensowanie danych do jednego DataFrame'a
if dataframes:
    # Łączenie wszystkich DataFrame'ów
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Zapisz do nowego pliku Excel
    output_file_path = os.path.join(folder_path, "combined_contacts.xlsx")
    combined_df.to_excel(output_file_path, index=False)

    print(f"Dane zostały skondensowane i zapisane w pliku: {output_file_path}")
else:
    print("Nie znaleziono żadnych plików z danymi do połączenia.")
    
# Combined Customers
# Ustawienie ścieżki do folderu z plikami Excel
folder_path = r"C:\Users\fabijans-1\OneDrive - Mettler Toledo LLC\All units task list\Data Quality\Weekly checks\Archive"  # Zmień tę ścieżkę

# Lista do przechowywania DataFrame'ów
dataframes = []

# Iteracja przez pliki w folderze i podfolderach
for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.endswith('.xlsx') and 'customers' in filename:
            file_path = os.path.join(dirpath, filename)
            
            # Wczytaj plik Excel
            try:
                df = pd.read_excel(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Nie udało się wczytać pliku {filename}: {e}")

# Skondensowanie danych do jednego DataFrame'a
if dataframes:
    # Łączenie wszystkich DataFrame'ów
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Zapisz do nowego pliku Excel
    output_file_path = os.path.join(folder_path, "combined_customers.xlsx")
    combined_df.to_excel(output_file_path, index=False)

    print(f"Dane zostały skondensowane i zapisane w pliku: {output_file_path}")
else:
    print("Nie znaleziono żadnych plików z danymi do połączenia.")