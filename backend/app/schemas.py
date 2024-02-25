from pydantic import BaseModel
from typing import List


class FilePathSchema(BaseModel):
    filePaths: List[str]
