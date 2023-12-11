from io import BytesIO

from pydantic import BaseModel


class PDFfile(BaseModel):
    id: str
    file: BytesIO