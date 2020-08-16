import pyodbc
import psycopg2
import uuid

from Models.DOI import DOI

class SQL:
    global is_postgres
    global server
    global database
    global username
    global password
    global cnxn
    global cursor



    def __init__(self):
        #set is_postgres variable 
        is_postgres = True

        if is_postgres:   #insert a environment variable check here 
            server = '127.0.0.1' 
            database = 'Resolver' 
            username = 'LanceTest' 
            password = 'asdTest123' 

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
        self.is_postgres = is_postgres
        self.cursor = cursor
        self.cnxn = cnxn


    def run_raw_sql(self, query):
        #Execute the SQL
        cursor.execute(query)
        return cursor.fetchone()


    def get_by(self, type, value):
        #self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '?'", asd)
        if type == "doi":
            if self.is_postgres:
                self.cursor.execute("SELECT * FROM \"TblDOI\" WHERE \"fDOI\" = '" + value + "' limit 1")
            else:
                self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOI = '" + value + "'")

            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "guid":
            if self.is_postgres:
                self.cursor.execute("SELECT * FROM \"TblDOI\" WHERE \"fGUID\" = '" + str(value) + "' limit 1")
            else:
                self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fGUID = " + value) 

            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "pkID":
            if self.is_postgres:
                self.cursor.execute("SELECT * FROM \"TblDOI\" WHERE \"fDOIID\" = '" + str(value) + "' limit 1") 
            else:
                self.cursor.execute("SELECT TOP 1 * FROM TblDOI WHERE fDOIID = '" + value + "'") 
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]


    def insert_doi(self, DOI_Post):
        # DOI_Entity.GUID = uuid.uuid4()
        self.cursor.execute("""INSERT INTO TblDOI (fDOI, fUserName, fPortalName, fXML, fView, fGUID) VALUES (?,?,?,?,?,?)""",
                        DOI_Post.doi, "Z10", "oa", DOI_Post.xml, DOI_Post.view, uuid.UUID(DOI_Post.guid))
        self.cnxn.commit()

        result = self.get_by("guid", DOI_Post.guid)
        
        DOI_Return = DOI(
            doiID = result[0],
            doi = result[1],
            user_name = result[2],
            portal_name = result[3],
            xml = result[4],
            view = result[5],
            guid = result[6]
        )

        if result:
            return DOI_Return
        else:
            return ["Error has occured"]


    def update_doi(self, DOI_Post: DOI):
        self.cursor.execute("UPDATE TblDOI SET fUserName = '" + DOI_Post.user_name + "', fPortalName = '" + DOI_Post.portal_name + "', fXML = '" + DOI_Post.xml + "', fView = '" + DOI_Post.view + "', fGUID = '" + DOI_Post.guid + "' WHERE fDOI = '" + DOI_Post.doi + "'")
        self.cnxn.commit()

        result = self.get_by("doi", DOI_Post.doi)

        #Map to DOI object
        DOI_Return = DOI(
            doiID = result[0],
            doi = result[1],
            user_name = result[2],
            portal_name = result[3],
            xml = result[4],
            view = result[5],
            guid = result[6]
        )

        if result:
            return DOI_Return
            #return result
        else:
            return ["Error has occured"]


    def add_doi_to_db(self, doi, user, portal, xml, view):
        rec_id = self.get_by("doi", doi)

        if rec_id != None:
            DOI_Insert = DOI(
                doiID = rec_id,
                doi = doi,
                user_name = user,
                portal_name = portal,
                xml = xml,
                view = view,
                guid = uuid.uuid4()
                )
            
            self.update_doi(DOI_Insert)
        else:
            DOI_Insert = DOI(
                doiID = 0,
                doi = doi,
                user_name = user,
                portal_name = portal,
                xml = xml,
                view = view,
                guid = uuid.uuid4()
                )
            
            self.insert_doi(DOI_Insert)
        
        result = self.get_by("doi", doi)
        
        DOI_Return = DOI(
            doiID = result[0],
            doi = result[1],
            user_name = result[2],
            portal_name = result[3],
            xml = result[4],
            view = result[5],
            guid = result[6]
        )

        return DOI_Return 