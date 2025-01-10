## Project Information

This project contains code that has been prepared for public release. To protect sensitive information, the following data has been removed or anonymized:
- Authentication credentials (e.g., API keys, passwords, tokens).
- Private user or company data.
- Sensitive environment configurations.

**Description:** Users are creating prospect accounts and contacts in SAP system. Data Stewards are getting excel report with newly generated prospects and contacts and they’re checking if users didn’t make any duplicates. Reports consist "Status" column, if account/contact was created properly it's value is "correct", if account/contact was created as duplicate it's value is "duplicate". Accounts and contacts are generated in two different excel files and will be classified in two different dashboards.

**Business objective:** Create KPI PowerBI Dashboard which will show how many accounts/contacts were made by each user but most important, how many were incorrect.

**Input:** Sharepoint with multiple xlsx files (reports with feedback from Data Stewards).

**Output:** SQL tables and PowerBI Dashboard.

## Data Processing
A few scripts were used to clean inconsistent columns in excel files:
- [checkcolumns.py](data_quality_checks_kpi_dashboard/checkcolumns.py) - used to search all unique columns in all excel files.
- [combinedfile_creation.py](data_quality_checks_kpi_dashboard/combinedfile_creation.py) - used to combine file with all unique columns added - helpful to check what columns have the same data.
- [updatecolumnsname.py](data_quality_checks_kpi_dashboard/updatecolumnsname.py) - changes columns based on dictionary (change old value to new value).

After data cleaning, the script for loading data into SQL and combining Excel files was created.**
- [dataload_sql_xlsx]() - saves already loaded files to not load it again. (IN PROCESS)

## PowerBI


