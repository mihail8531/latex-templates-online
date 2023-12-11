from settings import settings
from ..repository import BaseRepository
from schemas.s3 import PDFfile
from .s3 import S3
from io import BytesIO


class PDFRepository(BaseRepository[str, PDFfile]):
    def __init__(
        self, s3: S3 | None, pdf_files_bucket: str = settings.PDF_FILES_BUCKET
    ) -> None:
        if s3 is not None:
            assert pdf_files_bucket in s3.required_buckets
            self._s3 = s3
        else:
            self._s3 = S3(required_buckets=[pdf_files_bucket])

    def get_by_id(self, id: str) -> PDFfile:
        file = self._s3.download_file()
