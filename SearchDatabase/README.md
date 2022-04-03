## Azure Data Access Pipeline
### Fetch Data from Google, Bing and Twitter
Function takes in the list of keywords (pulls data from SQL by default) and the number of results to fetch as an argument.

### Azure Timer Trigger Functions
The function starts a CRON job that is scheduled at chosen time intervals (12 hours by default).
- Uses CRON expression in "function.json".

### Azure SQL
Data from the functions is inserted into the SQL Database that can be accessed through the server end-point. The end-point is open to all IP-Addresses for easy public access. Fetch on port 1433.