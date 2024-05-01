from repositories.repository import File, Repository


import aioboto3
from botocore.exceptions import ClientError


from io import BytesIO
from typing import Any


class S3Repository(Repository[File, str]):
    def __init__(
        self, bucket_name: str, url_expires_time: int, session: aioboto3.Session
    ):
        self.bucket_name = bucket_name
        self.url_expires_time = url_expires_time
        self.session = session

    async def get(self, id: str) -> File | None:
        async with self.session.resource("s3") as client:
            try:
                response = await client.get_object(Bucket=self.bucket_name, Key=id)
                data = response["Body"].read()
                return File(id=id, data=BytesIO(data))
            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchKey":
                    return None
                else:
                    raise

    async def get_download_url(self, id: str) -> str | None:
        async with self.session.resource("s3") as client:
            try:
                return await client.generate_presigned_url(
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
        async with self.session.resource("s3") as client:
            await client.put_object(
                Bucket=self.bucket_name, Key=item.id, Body=item.data.getvalue()
            )

    async def update(self, item: File, items: dict[str, Any]) -> None:
        await self.add(item)

    async def delete(self, item: File) -> None:
        async with self.session.resource("s3") as client:
            await client.delete_object(Bucket=self.bucket_name, Key=item.id)