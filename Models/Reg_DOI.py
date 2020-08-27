from typing import Optional

from pydantic import BaseModel
import uuid


class Reg_DOI(BaseModel):
    data: str
    view: str
    doi: str