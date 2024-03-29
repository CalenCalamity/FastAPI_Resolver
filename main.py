import DOI as DOI_Entity
import uuid

from MSSQL import MSSQL #Temp meassure till we get postgres going

from typing import Optional

from fastapi import FastAPI

app = FastAPI()
 
resolveURL = "http://app01.saeon.ac.za/get.aspx?guid=";

@app.get('/')
def home():
    return {"Status": "Home!"}

@app.get('/getdoi/')
def regdoi(doi: Optional[str] = ""):

    #return {"TEst":doi}
    # DOI_Entity.DOI = DOI_Post.DOI
    # DOI_Entity.UserName = "Z10"
    # DOI_Entity.PortalName = "oa"
    # DOI_Entity.View = DOI_Post.View
    # DOI_Entity.GUID = uuid.uuid4()

    #Check if DOI exists
    #DOI_Exists = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()
    DOI_Exists = MSSQL.get_by("doi", doi)[0] #Set the rec ID

    return {"doiid": DOI_Exists}

    if (DOI_Exists == 0):
        #Insert a new DOI
        '''
        Response.Write("add doi<br>");
        sql.insert("TblDOI");
        id = GetDOIID(con, doi);
        '''
        # session.add(DOI_Post)
        # session.commit()
        # inserted_Id = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()

        inserted_Id = MSSQL.insert_doi(DOI_Post)
    else:
        #Update an existing DOI
        '''
        Response.Write("edit doi<br>");
        sql.where("fDOIID", id);
        sql.edit("TblDOI");
        '''
        # session._update_impl(DOI_Post)
        # session.commit()
        # inserted_Id = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()
        inserted_Id = MSSQL.update_doi(DOI_Post)
    
    #Select the relevant GUID by the DOI_Exists Id
    '''
    sql.add("fDOIID", id);
    guid = sql.select("TblDOI", "fGUID").ToString();
    '''

    #session.query(DOI_Entity).filter_by(key=institution.parent_key).one() if institution.parent_key else None
    return {"GUID" : MSSQL.get_by("pkID", inserted_Id)}


@app .get("/get/{GUID}")
async def get_uuid(GUID: uuid.UUID):
    DOI_Exists = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()

    '''
    
            guid = new Guid().ToString();
            String query = "SELECT * FROM TblDOI WHERE fGUID = '" + guid.Replace("'", "''") + "'";
            view = set["fView"].ToString();
    '''

    view_URL = session.query(DOI_Entity).filter_by(UUID=GUID).one()
    return view_URL 