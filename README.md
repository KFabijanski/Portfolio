I am a Data Steward currently pursuing a Master's degree in Managerial Studies, with a strong passion for data science and technology. My interests extend beyond my enthusiasm for automotive culture; I am also keen on the stock market and cryptocurrencies.

After completing the Google Data Analytics Certificate, I discovered my fascination with data science, initially setting my sights on a data analyst role. However, my exploration of cloud computing and AWS during my coursework has inspired me to pursue a career as a Data Engineer.

I possess a solid understanding of SQL, familiarity with Power BI, and I am beginning my journey in Python programming. Additionally, I have foundational knowledge of various AWS services, including EC2, S3, DynamoDB, and RDS. In 2025, I am eager to secure a position that allows me to deepen my expertise and expand my knowledge in the data science field, propelling my career to new heights.

**Tools I like to use and my expertise level:**
1. SQL
- DQL (Data Query Language): Proficient in using ```SELECT``` statements, including complex queries with different types of ```JOIN``` (```INNER```, ```LEFT```, ```RIGHT```, ```FULL```).
- Familiar with clauses like ``GROUP BY``, ``HAVING``, ``WHERE``, and ``ORDER BY`` for data aggregation and filtering.
- Skilled in writing subqueries for advanced data retrieval and manipulation.
- Experienced in creating and modifying database structures (```CREATE TABLE```, ```ALTER TABLE```) and updating data with ```UPDATE``` and ```SET``` statements.
- Basic understanding of triggers (```CREATE TRIGGER```) and stored procedures (```CREATE PROCEDURE```) for automating database processes, with ongoing efforts to deepen knowledge in this area.
2. Python
- Basic understanding of Python programming and its application to data processing and automation.
- Initial experience in writing scripts to integrate and clean data from multiple sources, such as Excel files, with the support of AI tools.
- Currently learning data science libraries such as ```pandas```, ```SQLAlchemy```, and ```NumPy``` to enhance data manipulation and analysis skills.
3. Power BI
- Creating dashboards and reports to visualize data, tailored to business requirements.
- Data modelling: defining relationships between tables, setting up measures, calculated columns, and managing hierarchies.
- Basic knowledge of DAX: creating measures and calculations (e.g., ```SUM, AVERAGE, COUNT, IF, CALCULATE```).
- Integrating data from various sources, including Excel files, SQL databases, and cloud platforms.
- defining relationships between tables, setting up measures, calculated columns, and managing hierarchies.


**Recent projects:**
1. SLA KPI Dashboard - [SLA_KPI_Dashboard](main/SLA_KPI_Dashboard.md)
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
 
3. University project - python script **TO DO - will be visible in Github**
- 
