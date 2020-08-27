import uuid
from fastapi.testclient import TestClient

from ..main import app
#from ..SQL import SQL

client = TestClient(app)


def test_insert_item():
    response = client.post("/DOI", data={
            'doiID' : '0',
            'doi' : 'pytest_doi',
            'user_name' : 'pytest_username',
            'portal_name' : 'pytest_portalname',
            'xml' : 'pytest_xml',
            'view' : 'pytest_view',
            'guid' : str(uuid.uuid4)})

 #   sql_ret = SQL().get_by('doi', 'pytest_doi')[1]
    
    assert response.status_code == 200
  #  assert sql_ret == 'pytest_doi'
    #assert response.status_code


def test_update_item():
    response = client.put("/DOI", data={
            doiID : 0,
            doi : 'pytest_doi_new',
            user_name : 'pytest_username_new',
            portal_name : 'pytest_portalname_new',
            xml : 'pytest_xml_new',
            view : 'pytest_view_new',
            guid : str(uuid.uuid4)})
