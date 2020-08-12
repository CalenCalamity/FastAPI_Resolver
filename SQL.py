import pyodbc
import psycopg2

class SQL:
    global server
    global database
    global username
    global password
    global cnxn
    global cursor

    if False:   #insert a environment variable check here 
        cnxn = psycopg2.connect(user = username, #"sysadmin",
                                      password = password, # "pynative@#29",
                                      host = server, #"127.0.0.1",
                                      port = "5432",
                                      database = database) #"postgres_db")

    else:
        server = 'VEGA\SQLEXPRESS' 
        database = 'RESOLVER' 
        username = 'LanceDev' 
        password = 'asdTest123' 
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = cnxn.cursor()

    def run_raw_sql(query):
        #Execute the SQL
        cursor.execute(query)
        return cursor.fetchone()


    def get_by(type, value):
        #cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '?'", asd)
        if type == "doi":
            cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '" + value + "'") 
            result = cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "guid":
            cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fGUID = '" + value + "'") 
            result = cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "pkID":
            cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOIID = '" + value + "'") 
            result = cursor.fetchone()
            if result:
                return result
            else:
                return [0]


    def insert_doi(DOI_Post):
        # DOI_Entity.GUID = uuid.uuid4()
        cursor.execute("""INSERT INTO TblDOI (fDOI, fUserName, fPortalName, fXML, fView, fGUID) VALUES (?,?,?,?,?,?)""",
                        DOI_Post.DOI, "Z10", "oa", DOI_Post.xml, DOI_Post.view, DOI_Post.GUID)
        cnxn.commit()

        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return ["Error has occured"]


    def update_doi(DOI_Post):
        cursor.execute("UPDATE TblDOI SET fUserName = '" + DOI_Post.username + "', fPortalName = '" + DOI_Post.portalname + "', fXML = '" + DOI_Post.xml + "', fView = '" + DOI_Post.view + "', fGUID = '" + DOI_Post.GUID + "' WHERE fDOI = '" + DOI_Post.DOI + "'")
        cnxn.commit()

        result = self.get_by_doi(DOI_Post.DOI)[0]
        if result:
            return result[0]
        else:
            return ["Error has occured"]