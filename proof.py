# import pyodbc 
# server = 'VEGA\SQLEXPRESS' 
# database = 'Dev_DB' 
# username = 'LanceDev' 
# password = 'asdTest123' 
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
# print('Connected')

# #Sample select query
# cursor.execute("SELECT @@version;") 
# print(cursor.fetchone())



##############################################################################################################################################################################################################################

import requests


r = requests.put("http://127.0.0.1:8000/items/1", {"name": "string", "price": 0, "is_offer": True })
print(r.status_code, r.reason)
print(r.text[:300] + '...')