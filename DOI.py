import uuid
from typing import Optional

from pydantic import BaseModel

class DOI(BaseModel):
    DOIID: int
    DOI: str
    UserName: str
    PortalName: str
    View: str
    GUID: uuid.UUID