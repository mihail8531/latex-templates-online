from types_aiobotocore_s3 import S3ServiceResource
from repositories.repository import File, Repository


from botocore.exceptions import ClientError


from io import BytesIO
from typing import Any, ClassVar


class S3Repository(Repository[File, str]):
    bucket_name: ClassVar[str]
    url_expires_time: ClassVar[int]

    def __init__(self, s3_client: S3ServiceResource):
        self._s3_client = s3_client

    async def get(self, id: str) -> File | None:
        try:
            response = await self._s3_client.get_object(Bucket=self.bucket_name, Key=id)
            data = response["Body"].read()
            return File(id=id, data=BytesIO(data))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise

    async def get_download_url(self, id: str) -> str | None:
        try:
            return await self._s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": id},
                ExpiresIn=self.url_expires_time,
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise

    async def add(self, item: File) -> None:
        await self._s3_client.put_object(
            Bucket=self.bucket_name, Key=item.id, Body=item.data.getvalue()
        )

    async def update(self, item: File, items: dict[str, Any]) -> None:
        await self.add(item)

    async def delete(self, item: File) -> None:
        await self._s3_client.delete_object(Bucket=self.bucket_name, Key=item.id)
