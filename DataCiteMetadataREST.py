import requests

class DataCiteMetadataREST: 

    def __init__(self, username, password, uri = None):
        self.username = username
        self.password = password
        self.test_mode = False

        if uri is not None:
            self.uri = uri
        else:
            self.uri = "https://test.datacite.org/mds"


    def get_doi(self, doi):
        return self.make_request(self.uri + "/doi/" + doi)


    def set_doi(self, doi, url):
        message = "doi=" + doi + "\n"
        message += "url=" + url

        return self.make_request(self.uri + "/doi", "POST", message, "text/plaincharset=UTF-8")


    def get_metadata(self, doi):
        return self.make_request(self.uri + "/metadata/" + doi)


    def set_metadata(self, metadata):
        return self.make_request(self.uri + "/metadata", "POST", metadata, "application/xmlcharset=UTF-8")


    def delete_metadata(self, doi):
        return self.make_request(self.uri + "/doi/" + doi, "DELETE")


    def get_media(self, doi):
        return self.make_request(self.uri + "/media/" + doi)


    def set_media(self, doi, media_map):
        message = ""

        for m in media_map:
            if message != "":
                message += "\n"
            message += m.Key + "=" + m.Value

        return self.make_request(self.uri + "/media/" + doi, "POST", message, "text/plaincharset=UTF-8")


    def make_request(self, uri, method = "GET", message = "", contentType = "text/xml"):
        if self.test_mode:
            uri += "?test_mode=true"

        if method == "POST":
            response = requests.post(uri, data=message)
        elif method == "GET":
            response = requests.get(uri, data=message)
        
        return response