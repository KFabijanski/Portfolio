## Project Information

This project contains code that has been prepared for public release. To protect sensitive information, the following data has been removed or anonymized:
- Authentication credentials (e.g., API keys, passwords, tokens).
- Private user or company data.
- Sensitive environment configurations.

Description: Data Stewards are doing data modification tasks from requestors who sents them to shared outlook mailbox, then they use they own category to take this email and do the task, they have two working days to complete each task.

Business objective: Create KPI PowerBI Dashboard which will show how many requests each employee made with classification by “done in time” and “done in more than 2 working days.”

Input: MSSQL Database which downloads emails data from Outlook mailbox

Output: KPI PowerBI Dasboard

## SQL queries
Data needed for report is in two tables, one contains emails from done folders and second one does outlook snapshot with all cases in progress (it's done every 20 mins). Dashboard needs to count number of deduplicated request so **creating new columns with max date over each converstation id** is needed. Below two queries used for PowerBI are shown.

PowerBI Processed emails
```sql
SELECT uid, subject,  rcvddt AS receivedate, cnv_topic, MAX(rcvddt) OVER (PARTITION BY cnv_id) AS conversationmaxdate,
MAX(loadt) OVER (PARTITION BY cnv_id) AS loadmaxdate, [from], path, cnv_id, loadt AS loadtime, cats
FROM [dbo].[reporting_processed_emails]
WHERE [from] NOT LIKE 'mailbox@mailbox.com'
ORDER BY loadt DESC
```

PowerBI Inbox snap
```sql
SELECT uid, subject,  rcvddt AS receivedate, cnv_topic, MAX(rcvddt) OVER (PARTITION BY cnv_id) AS conversationmaxdate,
[from], path, cnv_id, loadt AS loadtime, cats
FROM [dbo].[reproting_inbox_snaps]
WHERE loadt = (SELECT MAX(loadt) FROM [dbo].[reproting_inbox_snaps])
```
Data is inserted into the SQL tables via a Python script. Categories need to directly reflect employee names; however, sometimes the SNOW category is used. Therefore, a trigger will be created to automate the cleaning process.

```sql
TRIGGER TO BE DONE
```

## PowerBI

## Final Dashboard:
![Dashboard_blurred](https://github.com/user-attachments/assets/d645e672-6fa4-4611-adc1-a3c6d234e8a8)
