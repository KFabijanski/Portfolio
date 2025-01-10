import os
import pandas as pd
 
# Path setting
folder_path = r"folderpath"  

# DataFrame list
dataframes = []

# Iteration through files in a folder and subfolders
for dirpath, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.endswith('.xlsx') and 'contacts' in filename:
            # Type the contacts or customers above in order to choose which type of reports you want to select
            file_path = os.path.join(dirpath, filename)
            
            # Load an Excel file
            try:
                df = pd.read_excel(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Failed to load a file {filename}: {e}")

# Consolidation of data into a single DataFrame
if dataframes:
    # Joining all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save to new Excel file
    output_file_path = os.path.join(folder_path, "combined_contacts.xlsx")
    combined_df.to_excel(output_file_path, index=False)

    print(f"The data has been compressed and saved in a file: {output_file_path}")
else:
    print("No data files for connection were found.")
