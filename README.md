#Run MySQL queries directly in Google Sheets

The script in this repo allows you to run SQL queries on a MySQL database from within a google sheet. You're able to execute the queries within cells in google sheets and designate which tabs the results should output to!

Steps to implement:

1) Go to tools -> script editor and copy paste the code
2) Fill in the db credentials
```
// Replace the variables in this block with real values.
var address = '';
var user = '';
var userPwd = '';
var db = '';
```
3) Save the script
4) Create a tab in your google sheet called 'tab_updates', the script will refer to this tab to look for queries
5) Create the following headers:

Tab;	Query;	Starting Column;	Update;	Status

6) Fill in each of the rows with the following data:

Tab - the name of the tab where you want the query output added (this name must exist in the sheet or the script will throw an error)
Query - The MySQL query that will return the data you want (I would test the query in workbench or the terminal first)
Starting - a number that represents which column of the tab you've designated where you want the data to start. Example: if you designate tab =  "Accounts" and Starting = "1" then the output of your query will start in cell A1. If you designate Starting = "5" then the output will start in cell E1 (the 5th column)
Update - Binary value, True or False which will tell the script whether to execute that particualr query when you run the script, or if you choose, it will igore it. This allows you to have many queries in many rows, but choose the ones you want to run at a given time by designating Update = "True"
Status - Leave this empty, the script will fill this cell with "success" or "fail" based on the result of the query

7) Once you've filled out all the columns (except the Status column) and have the right tabs created with the names you designated in the Tab column, execute the downloadData function. The google sheet prompt you to authenticate your google account, press accept and the data should appear in the designated location :+1:

This allows you to maintain data/dashboards that can be easily updated directly from a database. Another advantage is that you'll be able to reference the queries anytime you need to remind yourself of the conditions/filters which the data was queried

