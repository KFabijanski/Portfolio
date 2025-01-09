Recent projects:
1. SLA KPI Dashboard
- Description: Data Stewards are doing data modification tasks from requestors who sents them to shared outlook mailbox, then they use they own category to take this email and do the task, they have two working days to complete each task.
- Business objective: Create KPI PowerBI Dashboard which will show how many requests each employee made with classification by “done in time” and “done in more than 2 working days.”
-Input: MSSQL Database which downloads emails data from Outlook mailbox
-Output: KPI PowerBI Dasboard
- Most important steps:
  - Categories needed to be cleaned in SQL by using ```REPLACE()``` function. Changes made using ```UPDATE SET``` command.
  - Emails needed to be deduplicated in source data because PowerBI removes duplicate per every date not from whole dataset so it needed to be modified by creating receivedmaxdate column in SQL ```MAX(rcvddt) OVER (PARTITION BY cnv_topic)```.
  - Sales organizations were defined by creating groups of different paths, SLA measurement and table join were made with DAX.

2. Data Quality Checks KPI Dashboard:
- Description: Users are creating prospect accounts and contacts in SAP system. Data Stewards are getting excel report with newly generated prospects and contacts and they’re checking if users didn’t make any duplicates.
- Business objective: Create KPI PowerBI Dashboard which will show how many accounts/contacts were made by each user but most important, how many were incorrect.
- Input: Sharepoint with multiple xlsx files (reports with feedback from Data Stewards).
- Output: SQL tables and PowerBI Dashboard.
- Most important steps:
  - Reports were inconsistent when it comes to column names and schema, so names needed to be unified by python script using dictionary = {‘old name’: ‘new name’}, status column needed to be check file by file and data quality check process needed to be revised to be easy to measure.
  - Data was combined using python script and inserted into previously created SQL tables (functioning python script was done with help of AI tools). Script was designed to store already downloaded files and add new xlsx reports added to sharepoint, also data mapping was applied so SQL table will have always the same columns with no error.
 
3. University project - python script **TO DO**
- 
