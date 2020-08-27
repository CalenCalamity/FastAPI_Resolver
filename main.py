import uuid
import uvicorn

from html import escape, unescape
from SQL import SQL #Temp meassure
from DataCiteMetadataREST import DataCiteMetadataREST
from typing import Optional
from fastapi import FastAPI
from Models.DOI import DOI
from Models.Reg_DOI import Reg_DOI

app = FastAPI()
 
resolveURL = "http://app01.saeon.ac.za/get.aspx?guid="

@app.put("/DOI") #Needs to replace the get for the DOI although maybe keep the get for the existing services
async def update_item(DOI_Put: DOI):
    return SQL().update_doi(DOI_Put)


@app.post('/DOI')
async def create_institution(DOI_Post: DOI):
    return SQL().insert_doi(DOI_Post)


@app.post('/reg_doi')
async def register_doi(Post_Data: Reg_DOI):
    #Convert the `Data` to XML
    xml = Post_Data.data

    guid = SQL().add_doi_to_db(Post_Data.doi, "Z10", "oa", Post_Data.xml, Post_Data.view).guid
    url = resolveURL + escape(Post_Data.guid)

    client = DataCiteMetadataREST("NRF.TEST", "D@taC!te", "https://mds.test.datacite.org")
    metadata = client.set_metadata(Post_Data.xml)
    setDOI = client.set_doi(Post_Data.doi, url)

    return { 
        "URL" : client.uri,
        "Username" : client.username,
        "Password" : client.password,
        "Post Metadata" : metadata,
        "Update DOI URL" : setDOI
    }


@app.post('/resolve')
async def resolve(UUID: Optional[uuid.UUID]):
    if UUID == "":
        return {"Error" : "No UUID was provided"}
    else:
        return {"UUID" : UUID}



#Here we will keep all our get requests to accomadate the legacy dependencies
@app.get("/regdoi")
async def regdoi(data: Optional[str] = "", view: Optional[str] = "", doi: Optional[str] = ""):

    if doi == "" | data == "" | view == "":
        return { "Error" : "All 3 parameters require values"}

    #Convert the `Data` to XML
    xml = data

    guid = SQL().add_doi_to_db(doi, "Z10", "oa", xml, view).guid
    url = resolveURL + escape(guid)

    client = DataCiteMetadataREST("NRF.TEST", "D@taC!te", "https://mds.test.datacite.org")
    metadata = client.set_metadata(xml)
    setDOI = client.set_doi(doi, url)

    return { 
        "URL" : client.uri,
        "Username" : client.username,
        "Password" : client.password,
        "Post Metadata" : metadata,
        "Update DOI URL" : setDOI
    }


@app.get("/get")
async def get(GUID: Optional[uuid.UUID] = ""):

    result = SQL().get_by("guid", GUID)
    
    DOI_Return = DOI(
        doiID = result[0],
        doi = result[1],
        user_name = result[2],
        portal_name = result[3],
        xml = result[4],
        view = result[5],
        guid = result[6]
    )

    return {"View": DOI_Return.view}


@app.get("/resolve")
async def resolve_legacy(uuid: Optional[uuid.UUID] = ""):

    if uuid == "":
        return {"Error" : "No UUID was provided"}
    else:
        return {"UUID" : uuid}


#For Debug Purposes
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7000)