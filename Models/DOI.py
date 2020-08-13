from typing import Optional

from pydantic import BaseModel
import uuid


class DOI(BaseModel):
    doiID: int
    doi: str
    user_name: str
    portal_name: str
    xml: str
    view: str
    guid: str#uuid.UUID