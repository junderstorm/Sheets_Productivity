import pymysql
import pandas as pd
import sys
import os
import re #regex
from ast import literal_eval #to evalualte a string as a tuple
import pymysql.cursors  

#####
# The places where you would need to change in order to add fields:
#  getCsvData() - specifies file name, need to designate fields as floats or dates to interpret correctly
#               - also need to rename the field (the SFDC report name) to the MySQL table name
#####

def getConnection():
     '''function to connect to mySQL'''
    # You can change the connection arguments.
    connection = pymysql.connect(host='$localHostorIPAddress',
                                 user='$username',
                                 password='$pword',                             
                                 db='$dbname',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def getCsvData(csvName): 
	'''need to make sure names of headers and csv match params here
		make sure you explicitly declare the types of each column to increase read performance to Pandas '''
	data = pd.read_csv(
		csvName
		#,dtype={'numeric field': float} #example declaring a float
		#,parse_dates=['Date field'] #example declaring a date type
		)

	#Change the pandas column name from the csv name to the name of the column of the table you want to load to
	data.rename(columns = {
							'csv field name' : 'table name'
							,'csv field name2' : 'table name2'
							},inplace = True)

	return data

def getQuotes(string):
	''' this surrounds the value in double quotes - it also converts 'nan' values to blanks so that MySQL will convert to NULL
	    addditionally removes weird characters that will throw errors as they're attempted to be inserted'''
	if string == 'nan':
		return 'None'
	else: 
		return '"'+re.sub('[^A-Za-z0-9\.\[\]\s:-]+', '',string)+'"' 

def pandasToRows(df):
	rows = df.to_dict('index')
	return rows

def clearData(table_name):
	""" Truncate the data from a given table"""
	connection = myconnutils.getConnection() #this called the getconnection() function form the myconnutils file
	query = 'TRUNCATE TABLE '+table_name+';'
	cur = connection.cursor()
	try:
		cur.execute(query)
	except Exception as e: print(e) 
	connection.commit() #without nothing is written to the DB
	connection.close()
	print 'Cleared Data from:', table_name 		

def UploadAccountQuery(df,table_name):
	''' Create the INSERT Queries and return a data structure that can be iterated through to execute each query'''
	accountFields = df[0].keys()
	value_holder = '%s , '*len(accountFields)
	value_holder = '('+value_holder.rstrip(' ,')+')'
	query = 'INSERT INTO '+table_name + ' (' + ', '.join(accountFields)+ ') VALUES '+value_holder
	values_list = []
	for row in df:
		value_query = []
		for i in accountFields:
			append_element = getQuotes(str(df[row][i]))
			value_query.append(append_element)
		value_query = ','.join(value_query)
		values_list.append(value_query)	
	returnDicto = {'query':query,'values_list':values_list,'table':table_name}
	return returnDicto	

def insertFunction(query):
	''' this is the function that will write to the existing table 
	1) Row by run execute SQL INSERT - for problem rows return error and continue (will not crash)
	2) Commit changes and close conection '''

	#Getting the Insert string and the lists of values that will be written
	insertString = query['query']
	insertValueList = query['values_list']
	#Create variable for the count of rows and decrement for every INSERT statment that fails
	row_tracker = len(insertValueList)
	ticker = 0

	#call get connection for auth credentials
	connection = myconnutils.getConnection()
	print('Connect Successful!!')
	cur = connection.cursor()

	#Loop through the values and execute the insert statments one at a time, ignoring the ones that fail		
	for i in insertValueList:
		#incrementing as rows are writted in order to monitor status
		ticker += 1
		if ticker%1000 ==0: print '################ processed:', ticker
		#trying each INSERT statement so that if it fails the process will continue
		try:
			cur.execute(insertString,literal_eval(i))
		except Exception as e:
			print(e) 
			print(literal_eval(i))
			row_tracker -= 1

	connection.commit() #without nothing is written to the DB
	connection.close()
	print 'Connection Closed'
	print row_tracker, '/', len(insertValueList), round(row_tracker/float((len(insertValueList)))*100,2),'%', 'of rows succesfully written!'

if __name__ == "__main__":	
	#clearData('$csvName')  #Optional clear table
	df = pandasToRows(getCsvData('$csvName'))
	queryData =  UploadAccountQuery(df,'$tableName')
	insertFunction(queryData)
	
