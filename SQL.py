import pyodbc
import psycopg2

from Models.DOI import DOI

class SQL:
    global server
    global database
    global username
    global password
    global cnxn
    global cursor


    def __init__(self):
        if False:   #insert a environment variable check here 
            self.cnxn = psycopg2.connect(user = username, #"sysadmin",
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
        self.cursor = cursor
        self.cnxn = cnxn


    def run_raw_sql(self, query):
        #Execute the SQL
        cursor.execute(query)
        return cursor.fetchone()


    def get_by(self, type, value):
        #self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '?'", asd)
        if type == "doi":
            self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '" + value + "'") 
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "guid":
            self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fGUID = '" + value + "'") 
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "pkID":
            self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOIID = '" + value + "'") 
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]


    def insert_doi(self, DOI_Post):
        # DOI_Entity.GUID = uuid.uuid4()
        self.cursor.execute("""INSERT INTO TblDOI (fDOI, fUserName, fPortalName, fXML, fView, fGUID) VALUES (?,?,?,?,?,?)""",
                        DOI_Post.doi, "Z10", "oa", DOI_Post.xml, DOI_Post.view, DOI_Post.guid)
        self.cnxn.commit()

        result = self.get_by("guid", DOI_Post.gupycgharmid)
        if result:
            return result[0]
        else:
            return ["Error has occured"]


    def update_doi(self, DOI_Post: DOI):
        self.cursor.execute("UPDATE TblDOI SET fUserName = '" + DOI_Post.user_name + "', fPortalName = '" + DOI_Post.portal_name + "', fXML = '" + DOI_Post.xml + "', fView = '" + DOI_Post.view + "', fGUID = '" + DOI_Post.guid + "' WHERE fDOI = '" + DOI_Post.doi + "'")
        self.cnxn.commit()

        result = self.get_by("doi", DOI_Post.doi)[0]
        if result:
            return result
        else:
            return ["Error has occured"]