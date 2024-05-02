from typing import TYPE_CHECKING, AsyncGenerator
from types_aiobotocore_s3 import S3ServiceResource
from aioboto3 import Session
from fastapi import Depends
from settings import settings

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3ServiceResource
else:
    S3ServiceResource = Any

def get_s3_session(
    aws_access_key_id: str | None = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key: str | None = settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token: str | None = settings.AWS_SESSION_TOKEN,
    region_name: str | None = settings.REGION_NAME,
) -> Session:
    return Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )


async def get_s3_client(
    session: Session = Depends(get_s3_session),
) -> AsyncGenerator[S3ServiceResource, None]:
    async with session.resource("s3") as client:
        yield client
