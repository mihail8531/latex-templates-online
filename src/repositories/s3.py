from types_aiobotocore_s3 import S3Client
from repositories.repository import File, Repository
import urllib.parse


from botocore.exceptions import ClientError


from io import BytesIO
from typing import Any, ClassVar


class S3Repository(Repository[File, str]):
    bucket_name: ClassVar[str]
    url_expires_time: ClassVar[int]
    outer_endpoint_url_host: ClassVar[str | None]

    def __init__(self, s3_client: S3Client):
        self._s3_client = s3_client

    async def get(self, id: str) -> File | None:
        try:
            response = await self._s3_client.get_object(Bucket=self.bucket_name, Key=id)
            data = await response["Body"].read()
            return File(id=id, data=BytesIO(data))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise

    def fix_url_host(self, url: str) -> str:
        if self.outer_endpoint_url_host is None:
            return url
        parsed = urllib.parse.urlparse(url)
        replaced = parsed._replace(netloc=self.outer_endpoint_url_host)
        return replaced.geturl()

    async def get_download_url(
        self, id: str, filename: str, pdf_show: bool = False
    ) -> str | None:
        try:
            url = await self._s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": id,
                    "ResponseContentDisposition": f"attachment; filename = {filename}",
                    **(
                        {
                            "ResponseContentDisposition": f"inline; filename = {filename}",
                            "ResponseContentType": "application/pdf",
                        }
                        if pdf_show
                        else {}
                    ),
                },
                ExpiresIn=self.url_expires_time,
            )
            return self.fix_url_host(url)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise

    async def add(self, item: File) -> None:
        await self._s3_client.upload_fileobj(item.data, self.bucket_name, item.id)

    async def update(self, item: File, items: dict[str, Any]) -> None:
        await self.add(item)

    async def delete(self, item: File) -> None:
        await self._s3_client.delete_object(Bucket=self.bucket_name, Key=item.id)
