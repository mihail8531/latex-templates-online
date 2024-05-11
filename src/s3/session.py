from typing import TYPE_CHECKING, AsyncGenerator
from types_aiobotocore_s3 import S3Client
from aioboto3 import Session
from fastapi import Depends
from settings import settings

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3ServiceResource
else:
    from typing import Any

    S3ServiceResource = Any


def get_s3_session() -> Session:
    return Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_REGION_NAME,
    )


async def get_s3_client(
    session: Session = Depends(get_s3_session),
) -> AsyncGenerator[S3Client, None]:
    async with session.client("s3", endpoint_url=settings.AWS_ENDPOINT_URL) as client:
        yield client
