import html
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import Optional

from ..db import db_session
from ..models.DOI import DOI
from ..models.Reg_DOI import Reg_DOI
from ..DataCiteMetadataREST import DataCiteMetadataREST
from ..SQL import SQL

router = APIRouter()

 
resolveURL = "http://app01.saeon.ac.za/get.aspx?guid="

@router.put("/DOI")
async def update_item(DOI_Put: DOI):
    return SQL().update_doi(DOI_Put)


@router.post('/DOI')
async def insert_item(DOI_Post: DOI):
    return SQL().insert_doi(DOI_Post)


@router.post('/reg_doi')
async def register_doi(Post_Data: Reg_DOI):
    #Convert the `Data` to XML
    xml = Post_Data.data

    guid = SQL().add_doi_to_db(Post_Data.doi, "Z10", "oa", xml, Post_Data.view).guid
    url = resolveURL + html.escape(guid)

    client = DataCiteMetadataREST("NRF.TEST", "D@taC!te", "https://mds.test.datacite.org")
    metadata = client.set_metadata(xml, Post_Data.doi)
    setDOI = client.set_doi(Post_Data.doi, url)

    return { 
        "URL" : client.uri,
        "Username" : client.username,
        "Password" : client.password,
        "Post Metadata" : metadata,
        "Update DOI URL" : setDOI
    }


@router.post('/resolve')
async def resolve(uuid: Optional[str] = ""):
    if uuid == "" or uuid == '':
        raise HTTPException(status_code=422, detail="No UUID was provided")
    elif not SQL().is_valid_uuid(uuid):
        raise HTTPException(status_code=422, detail="Invalid UUID was provided")
    else:
        return {"UUID" : uuid}



#Here we will keep all our get requests to accomadate the legacy dependencies
@router.get("/regdoi.aspx")
async def regdoi(data: Optional[str] = '', view: Optional[str] = '', doi: Optional[str] = ''):

    if doi == '' or data == '' or view == '':
        return { "Error" : "All 3 parameters require values"}

    #Convert the `Data` to XML
    xml = data

    guid = SQL().add_doi_to_db(doi, "Z10", "oa", xml, view).guid
    url = resolveURL + html.escape(guid)

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


@router.get("/get.aspx")
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


@router.get("/resolve.aspx")
async def resolve_legacy(uuid: Optional[str] = ""):
    if uuid == "" or uuid == '':
        raise HTTPException(status_code=422, detail="No UUID was provided")
    elif not SQL().is_valid_uuid(uuid):
        raise HTTPException(status_code=422, detail="Invalid UUID was provided")
    else:
        return {"UUID" : uuid}
