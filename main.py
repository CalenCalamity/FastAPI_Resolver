import uuid
import uvicorn

from SQL import SQL #Temp meassure
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from Models.DOI import DOI

app = FastAPI()
 
resolveURL = "http://app01.saeon.ac.za/get.aspx?guid="

@app.put("/DOI") #Needs to replace the get for the DOI although maybe keep the get for the existing services
async def update_item(DOI_Put: DOI):
    return SQL().update_doi(DOI_Put)


@app.post('/DOI')
async def create_institution(DOI_Post: DOI):
    return SQL().insert_doi(DOI_Post)


@app.post('/reg_doi')
async def register_doi(DOI: str):
    return { "Result": DOI }



@app.post('/reg_doi_xml')
async def register_doi_xml(DOI: str):
    return { "Result": DOI }


@app.post('/resolve')
async def resolve(DOI: str):
    return { "Result": DOI }


@app.get('/')
def home():
    return {"Status": "Home!"}


#Here we will keep all our get requests to accomadate the legacy dependencies

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
    DOI_Exists = SQL().get_by("doi", doi)[0] #Set the rec ID

    return {"doiid": DOI_Exists}

    if (DOI_Exists == 0):
        #Insert a new DOI
        '''
        Response.Write("add doi<br>");
        SQL().insert("TblDOI");
        id = GetDOIID(con, doi);
        '''
        # session.add(DOI_Post)
        # session.commit()
        # inserted_Id = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()

        inserted_Id = SQL().insert_doi(DOI_Post)
    else:
        #Update an existing DOI
        '''
        Response.Write("edit doi<br>");
        SQL().where("fDOIID", id);
        SQL().edit("TblDOI");
        '''
        # session._update_impl(DOI_Post)
        # session.commit()
        # inserted_Id = session.query(DOI_Entity).filter_by(DOI=DOI_Post.DOI).one()
        inserted_Id = SQL().update_doi(DOI_Post)
    
    #Select the relevant GUID by the DOI_Exists Id
    '''
    SQL().add("fDOIID", id);
    guid = SQL().select("TblDOI", "fGUID").ToString();
    '''

    #session.query(DOI_Entity).filter_by(key=institution.parent_key).one() if institution.parent_key else None
    return {"GUID" : SQL().get_by("pkID", inserted_Id)}


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


#For Debug Purposes
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7000)