import uuid
import json
from fastapi.testclient import TestClient

from resolverapi import app
from resolverapi.SQL import SQL

client = TestClient(app)


def test_insert_item():
    response = client.post("/DOI", json={
      "doiID" : 0,
      "doi" : "10.5438/0012",
      "user_name" : "NRF.TEST",
      "portal_name" : "pytest_portalname",
      "xml" : "pytest_xml",
      "view" : "pytest_view",
      "guid" : "98f44ff4-575c-4640-b6a5-ee6101c844a0"})

    sql_ret = SQL().get_by('guid', '98f44ff4-575c-4640-b6a5-ee6101c844a0')[1]
    assert response.status_code == 200
    assert sql_ret == '10.5438/0012'


def test_update_item():
    response = client.put("/DOI", json={
      "doiID" : 0,
      "doi" : "10.5438/0012",
      "user_name" : "pytest_username_new",
      "portal_name" : "pytest_portalname_new",
      "xml" : "<resource xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://datacite.org/schema/kernel-4\" xsi:schemaLocation=\"http://datacite.org/schema/kernel-4 http://schema.datacite.org/meta/kernel-4/metadata.xsd\"><identifier identifierType=\"DOI\">10.5438/0012</identifier><creators><creator><creatorName nameType=\"Personal\">Test, Example</creatorName><givenName>Example</givenName><familyName>Example</familyName></creator></creators><titles><title>Example</title></titles><publisher>DataCite</publisher><publicationYear>2020</publicationYear><resourceType resourceTypeGeneral=\"Dataset\"/><sizes/><formats/><version/></resource>",
      "view" : "pytest_view_new",
      "guid" : "98f44ff4-575c-4640-b6a5-ee6101c844a0"})

    sql_ret = SQL().get_by('guid', '98f44ff4-575c-4640-b6a5-ee6101c844a0')
    assert response.status_code == 200
    assert sql_ret[4] != 'pytest_xml'
    assert sql_ret[1] == '10.5438/0012'


def test_resolve():
  guid = "98f44ff4-575c-4640-b6a5-ee6101c844a0"
  
  response = client.post(f'/resolve?uuid={guid}')
  resp_obj = json.loads(response.content)
  assert response.status_code == 200 
  assert resp_obj['UUID'] == guid

  response = client.post('/resolve?uuid=')
  resp_obj = json.loads(response.content)
  assert response.status_code == 422
  assert resp_obj['detail'] == "No UUID was provided"

  response = client.post(f'/resolve?uuid={123}')
  resp_obj = json.loads(response.content)
  assert response.status_code == 422
  assert resp_obj['detail'] == "Invalid UUID was provided"


#Tests for legacy endpoints
def test_get_legacy():
  response = client.get('/get.aspx?GUID=98f44ff4-575c-4640-b6a5-ee6101c844a0')
  
  resp_obj = json.loads(response.content)

  assert resp_obj['View'] == "pytest_view_new"
  assert response.status_code == 200


def test_resolver_legacy():
  guid = "98f44ff4-575c-4640-b6a5-ee6101c844a0"
  
  response = client.get(f'/resolve.aspx?uuid={guid}')
  resp_obj = json.loads(response.content)
  assert response.status_code == 200 
  assert resp_obj['UUID'] == guid

  response = client.get('/resolve.aspx?uuid=')
  resp_obj = json.loads(response.content)
  assert response.status_code == 422
  assert resp_obj['detail'] == "No UUID was provided"

  response = client.get(f'/resolve.aspx?uuid={123}')
  resp_obj = json.loads(response.content)
  assert response.status_code == 422
  assert resp_obj['detail'] == "Invalid UUID was provided"


def test_clean():
  uuid = '98f44ff4-575c-4640-b6a5-ee6101c844a0'
  response = SQL().delete_by_guid(uuid)

  assert response == True