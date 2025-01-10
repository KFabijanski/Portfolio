## Project Information

This project contains code that has been prepared for public release. To protect sensitive information, the following data has been removed or anonymized:
- Authentication credentials (e.g., API keys, passwords, tokens).
- Private user or company data.
- Sensitive environment configurations.

**Description:** Data Stewards are doing data modification tasks from requestors who sents them to shared outlook mailbox, then they use their own name's category to take this email and do the task, they have two working days to complete each task.

**Business objective:** Create KPI PowerBI Dashboard which will show how many requests each employee made with classification by “done in time” and “done in more than 2 working days.”

**Input:** MSSQL Database which downloads emails data from Outlook mailbox

**Output:** KPI PowerBI Dasboard

## SQL queries
Data needed for report is in two tables, one contains emails from done folders and second one does outlook snapshot with all cases in progress (it's done every 20 mins). 

Cats data cleaning was processed using REPLACE() function:
```sql
UPDATE [dbo].[reporting_processed_emails]
SET cats = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    cats,
    'CCT, ', ''),
    'CRM, ', ''),
    'SNOW, ', ''),
    ', SNOW', ''),
    ', CRM', ''),
    ', CCT', ''),
    'CCT', ''),
    'SNOW', ''),
    'CRM', ''),
    '', ''),
    'Magda S-K', 'DS Magda S'),
    'FINANCE, ', ''),
    'BVT Testing, ', ''),
    'FINANCE', ''),
    'mass', ''),
    ', FINANCE', ''),
    'On hold', ''),
    'Waiting for an answer, ', '');
```

PowerBI Processed emails
```sql
SELECT uid, subject,  rcvddt AS receivedate, cnv_topic, MAX(rcvddt) OVER (PARTITION BY cnv_id) AS conversationmaxdate,
MAX(loadt) OVER (PARTITION BY cnv_id) AS loadmaxdate, [from], path, cnv_id, loadt AS loadtime, cats
FROM [dbo].[reporting_processed_emails]
WHERE [from] NOT LIKE 'datastewardsmailbox@mailbox.com'
ORDER BY loadt DESC;
```
Dashboard needs to count number of deduplicated request so **creating new columns with max date over each converstation id** is needed. Below two queries used for PowerBI are shown.

PowerBI Inbox snap
```sql
SELECT uid, subject,  rcvddt AS receivedate, cnv_topic, MAX(rcvddt) OVER (PARTITION BY cnv_id) AS conversationmaxdate,
[from], path, cnv_id, loadt AS loadtime, cats
FROM [dbo].[reporting_inbox_snaps]
WHERE loadt = (SELECT MAX(loadt) FROM [dbo].[reporting_inbox_snaps]);
```
Data is inserted into the SQL tables via a Python script. Categories need to directly reflect employee names; however, sometimes the SNOW category is used. Therefore, a trigger will be created to automate the cleaning process.

TRIGGER [dbo].[reproting_inbox_snaps]
```sql
CREATE TRIGGER reproting_inbox_snaps_clean
ON [dbo].[reproting_inbox_snaps]
AFTER INSERT
AS
BEGIN
	UPDATE [dbo].[reproting_inbox_snaps]
	SET cats = REPLACE(REPLACE(REPLACE(REPLACE(
		cats,
		'CCT, ', ''),
		', CCT',''),
		'SNOW, ',''),
		', SNOW','')
	WHERE uid IN (SELECT uid FROM Inserted);
END;
```
TRIGGER [dbo].[reproting_processed_emails]
```sql
CREATE TRIGGER reporting_processed_emails_clean
ON [dbo].[reproting_processed_emails]
AFTER INSERT
AS
BEGIN
	UPDATE [dbo].[reproting_processed_emails]
	SET cats = REPLACE(REPLACE(REPLACE(REPLACE(
		cats,
		'CCT, ', ''),
		', CCT',''),
		'SNOW, ',''),
		', SNOW','')
	WHERE uid IN (SELECT uid FROM Inserted);
END;
```

TRIGGER CHECK
```sql
SELECT 
    t.name AS TriggerName,
    OBJECT_NAME(t.parent_id) AS TableName,
    t.type_desc AS TriggerType,
    t.create_date,
    t.modify_date
FROM 
    sys.triggers t
ORDER BY 
    TableName, TriggerName;
```
## PowerBI
Creating combined table in DAX which will be used to track done and in progress tasks.
```DAX
CombinedCustomerInboxTable = UNION(
    SELECTCOLUMNS(
        Processed,
        "uid", Processed[uid],
        "subject", Processed[subject],
        "receivedate", Processed[receivedate],
        "cnv_topic", Processed[cnv_topic],
        "conversationmaxdate", Processed[conversationmaxdate],
        "from", Processed[from],
        "path", Processed[path],
        "cnv_id", Processed[cnv_id],
        "loadtime", Processed[loadtime],
        "cats", Processed[cats]
    ),
    SELECTCOLUMNS(
        Inbox_snaps,
        "uid", Inbox_snaps[uid],
        "subject", Inbox_snaps[subject],
        "receivedate", Inbox_snaps[receivedate],
        "cnv_topic", Inbox_snaps[cnv_topic],
        "conversationmaxdate", Inbox_snaps[conversationmaxdate],
        "from", Inbox_snaps[from],
        "path", Inbox_snaps[path],
        "cnv_id", Inbox_snaps[cnv_id],
        "loadtime", Inbox_snaps[loadtime],
        "cats", Inbox_snaps[cats]
    )
)
```
Sales_unit and Staus values were made using grouping path

Task type shows if task was a customer creation or customer change - logic points types of words used in creation forms and the rest is classified as change.
```DAX
Task type = IF(CONTAINSSTRING(CombinedCustomerInboxTable[subject], "New Material")
||CONTAINSSTRING(CombinedCustomerInboxTable[subject],"Creation")
||CONTAINSSTRING(CombinedCustomerInboxTable[subject],"New Customer")
||CONTAINSSTRING(CombinedCustomerInboxTable[subject],"MT.com Request")
||CONTAINSSTRING(CombinedCustomerInboxTable[subject],"GNF Routed")
||CONTAINSSTRING(CombinedCustomerInboxTable[subject],"MT.com Anfrage"),"Creation","Change")
```

SLA is measured in 3 steps, employee needs to do a task within two working days.
SLA_1 - calculates the number of working days between the maximum conversation date and the maximum load date, excluding the start date.
```DAX
C_SLA = NETWORKDAYS(Processed[conversationmaxdate],Processed[loadmaxdate])-1
```
SLA_1.5 - adds exceptions, if subject contains any of those works they are automatically assignned as 1.
```DAX
C_SLA1.5 = if(CONTAINSSTRING(Processed[subject],"archive")
|| CONTAINSSTRING(Processed[subject],"archiving")
|| CONTAINSSTRING(Processed[subject],"I-Base")
|| CONTAINSSTRING(Processed[subject],"Change later")
|| CONTAINSSTRING(Processed[subject],"inactivation")
|| CONTAINSSTRING(Processed[subject],"merge")
|| CONTAINSSTRING(Processed[subject],"block")
|| CONTAINSSTRING(Processed[subject],"duplicate"),1,NETWORKDAYS(Processed[conversationmaxdate],Processed[loadmaxdate])-1)
```
SLA_2 - labels data with two categories "<=2wD" and ">2wD".
```DAX
C_SLA2 = IF(Processed[C_SLA1.5]<3,"<=2wD",">2wD")
```

## Final Dashboard:
For sensitive data reasons, whole dashboard cannot be shown but below is one of pages with blurred data.
![Dashboard_blurred](https://github.com/user-attachments/assets/d645e672-6fa4-4611-adc1-a3c6d234e8a8)
