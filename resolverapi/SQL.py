import psycopg2
import uuid

from resolverapi.models.DOI import DOI

class SQL:
    global is_postgres
    global server
    global database
    global username
    global password
    global cnxn
    global cursor


    def __init__(self):

        server = '127.0.0.1' 
        database = 'Resolver' 
        username = 'postgres' 
        password = 'asdTest123' 

        cnxn = psycopg2.connect(user = username,
                                password = password,
                                host = server,
                                port = "5432",
                                database = database)

        cursor = cnxn.cursor()
        self.cursor = cursor
        self.cnxn = cnxn


    def run_raw_sql(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()


    def get_by(self, type, value):
        if type == "doi":
            self.cursor.execute("SELECT * FROM \"tbldoi\" WHERE \"fDOI\" = '" + value + "' limit 1")

            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "guid":
            self.cursor.execute("SELECT * FROM \"tbldoi\" WHERE \"fGUID\" = '" + str(value) + "' limit 1")

            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]
        elif type == "pkID":
            self.cursor.execute("SELECT * FROM \"tbldoi\" WHERE \"fDOIID\" = '" + str(value) + "' limit 1") 

            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return [0]


    def insert_doi(self, DOI_Post):
        if DOI_Post.guid == "":
            DOI_Post.guid == uuid.uuid4()
        elif not self.is_valid_uuid(DOI_Post.guid):
            return ["Error, invalid GUID"]

        self.cursor.execute(f"""INSERT INTO \"tbldoi\" (\"fDOI\", \"fUserName\", \"fPortalName\", \"fXML\", \"fView\", \"fGUID\") VALUES (\'{DOI_Post.doi}\', \'Z10\', \'oa\', \'{DOI_Post.xml}\', \'{DOI_Post.view}\', \'{str(DOI_Post.guid)}\')""")
        self.cnxn.commit()

        result = self.get_by("guid", DOI_Post.guid)
        
        DOI_Return = DOI(
            doiID = result[0],
            doi = result[1],
            user_name = result[2],
            portal_name = result[3],
            xml = result[4],
            view = result[5],
            guid = result[6])

        if result:
            return DOI_Return
        else:
            return ["Error has occured"]


    def update_doi(self, DOI_Post: DOI):
        self.cursor.execute("UPDATE \"tbldoi\" SET \"fUserName\" = '" + DOI_Post.user_name + "', \"fPortalName\" = '" + DOI_Post.portal_name + "', \"fXML\" = '" + DOI_Post.xml + "', \"fView\" = '" + DOI_Post.view + "', \"fDOI\" = '" + DOI_Post.doi + "' WHERE \"fGUID\" = '" + DOI_Post.guid + "'")
            
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
        else:
            return ["Error has occured"]


    def add_doi_to_db(self, doi, user, portal, xml, view):
        rec_id = self.get_by("doi", doi)

        if rec_id[0] != 0:
            DOI_Insert = DOI(
                doiID = rec_id[0],
                doi = doi,
                user_name = user,
                portal_name = portal,
                xml = xml,
                view = view,
                guid = rec_id[6]
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


    def is_valid_uuid(self ,uuid_to_test, version=4):
        """
        Check if uuid_to_test is a valid UUID.

        Parameters
        ----------
        uuid_to_test : str
        version : {1, 2, 3, 4}

        Returns
        -------
        `True` if uuid_to_test is a valid UUID, otherwise `False`.
        """
        try:
            val = uuid.UUID(uuid_to_test)
        except ValueError:
            return False

        return True
    

    def delete_by_guid(self, guid):
        self.cursor.execute(f"delete from \"tbldoi\" where \"fGUID\" = '{guid}';")
        self.cnxn.commit()

        if self.get_by('guid', guid) == [0]:
            return True
        else:
            return False
