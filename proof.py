import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'VEGA\SQLEXPRESS' 
database = 'Dev_DB' 
username = 'LanceDev' 
password = 'asdTest123' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print('Connected')

#Sample select query
cursor.execute("SELECT @@version;") 
print(cursor.fetchone())
# row = cursor.fetchone() 
# while row: 
#     print(row[0])
#     row = cursor.fetchone()