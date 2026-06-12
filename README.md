I am a Reporting Specialist / BI Developer working with ThoughtSpot and Google Cloud Platform, focused on building and maintaining end-to-end data solutions for business users.

In my current role, I operate as a full owner of the analytics layer — from data sourcing and transformation in BigQuery, through modeling and liveboards in ThoughtSpot, to supporting business users and resolving data quality issues. I work closely with stakeholders to ensure data consistency, troubleshoot discrepancies, and maintain trust in reporting.

I have hands-on experience with GCP, primarily BigQuery, where I create and maintain views used for analytics. I also contribute to maintaining internal data tooling (cdp-tool), including debugging Cloud Build issues, managing upgrades, and supporting deployment processes. Additionally, I have worked with Terraform (e.g., creating storage buckets), service accounts, and basic cloud security practices such as key rotation.

My work includes exposure to orchestration tools like Airflow (DAG-based transformations), as well as building lightweight automation solutions using Python and Power Automate to improve data validation and reporting workflows.

On the frontend side, I design and manage ThoughtSpot models, worksheets, and liveboards, often integrating multiple data sources and implementing row-level security (RLS). I also built a custom internal web application using JavaScript to embed and visualize ThoughtSpot data in alternative formats (Echarts - Race charts).

**Tech Stack & Skills:**
1. SQL
- Advanced querying (CTEs, joins, aggregations)
- Working with large-scale datasets (millions of records, GB-scale queries)
- Data transformation using BigQuery views
- Basic exposure to window functions
2. GCP
- BigQuery (core data layer)
- Cloud Build (CI/CD troubleshooting and maintenance)
- Terraform (basic infrastructure setup)
- Service accounts and access management
3. ThoughtSpot
- Data modeling (worksheets, joins, relationships)
- Liveboard and dashboard development
- Row-level security (RLS) implementation
- Data validation and troubleshooting with business users
4. Python
- Basic automation and data validation scripts
- Data comparison and QA support tools
- Working with Excel-based data pipelines
5. Additional
- Airflow (basic DAG-based transformations)
- Power Automate (workflow automation)
- Other BI Tools: Power BI(proven experience), Tableu and Looker (used at trainings)
- AWS (used at trainings)
- JavaScript (internal data visualization tool using embedded analytics and ECharts)
6. Additional BI Tools
- Power BI (hands-on experience in dashboarding and data modeling)
- Tableau, Looker (basic familiarity)
7. Cloud & Data Platforms
- GCP (primary environment – BigQuery, Cloud Build, IAM)
- Oracle (legacy system support, data removal and maintenance tasks)
- MSSQL (hands-on experience)
- AWS (basic familiarity)

I am currently focused on transitioning into a Data Engineer role, with a strong interest in building scalable data pipelines, improving data infrastructure, and working more deeply with cloud-based data processing.

**Recent projects:**
1. Otomoto Data Scraping & Analytics Pipeline (WIP):
- Planned GCP-based pipeline for collecting, storing, and analyzing car listing data from Otomoto.
- Focus on tracking price trends and building a structured dataset for analytical queries.

2. Excel QA Tool - [here](excel_qa_tool/Introduction.md):
- Description: Tool designed to compare two Excel datasets and detect row-level inconsistencies across multiple sheets. It is used for data quality validation and reconciliation of reporting outputs in BI environments.
- Business objective: Ensure data consistency and reliability across reporting datasets by identifying discrepancies between different Excel extracts used in BI reporting and analytics workflows.
-Input: Two Excel files containing reporting or analytical datasets exported from source systems or BI tools.
-Output: List of detected differences between datasets, including missing or mismatched rows across sheets.
- Most important steps:
  - Data normalization to handle inconsistencies such as date formats, whitespace variations, and text formatting differences.
  - Filtering out technical or irrelevant export metadata rows.
  - Row-level comparison across multiple sheets using a deduplication-aware logic.
  - Detection of differences using aggregated row counts and comparison logic (Counter-based matching).
  - Optional debug mode for deeper analysis of data discrepancies and potential root causes.
 
3. SLA KPI Dashboard - [here](sla_kpi_dashboard/SLA_KPI_Dashboard.md):
- Description: Data Stewards are doing data modification tasks from requestors who sents them to shared outlook mailbox, then they use they own category to take this email and do the task, they have two working days to complete each task.
- Business objective: Create KPI PowerBI Dashboard which will show how many requests each employee made with classification by “done in time” and “done in more than 2 working days.”
-Input: MSSQL Database which downloads emails data from Outlook mailbox
-Output: KPI PowerBI Dasboard
- Most important steps:
  - Categories needed to be cleaned in SQL by using ```REPLACE()``` function. Changes made using ```UPDATE SET``` command.
  - Emails needed to be deduplicated in source data because PowerBI removes duplicate per every date not from whole dataset so it needed to be modified by creating receivedmaxdate column in SQL ```MAX(rcvddt) OVER (PARTITION BY cnv_topic)```.
  - Sales organizations were defined by creating groups of different paths, SLA measurement and table join were made with DAX.

4. Data Quality Checks KPI Dashboard - [here](data_quality_checks_kpi_dashboard/Introduction.md):
- Description: Users are creating prospect accounts and contacts in SAP system. Data Stewards are getting excel report with newly generated prospects and contacts and they’re checking if users didn’t make any duplicates.
- Business objective: Create KPI PowerBI Dashboard which will show how many accounts/contacts were made by each user but most important, how many were incorrect.
- Input: Sharepoint with multiple xlsx files (reports with feedback from Data Stewards).
- Output: Combined xlsx files and PowerBI Dashboard.
- Most important steps:
  - Reports were inconsistent when it comes to column names and schema, so names needed to be unified by python script using dictionary = {‘old name’: ‘new name’}, status column needed to be check file by file and data quality check process needed to be revised to be easy to measure.
  - Data was combined using python script and inserted into combined xlsx. Script was designed to store already downloaded files and add new xlsx reports added to sharepoint, also data mapping was applied so PowerBI table will have always the same columns with no error.
 
