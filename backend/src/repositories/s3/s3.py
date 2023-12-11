import boto3
from typing import Sequence
import botocore
import mimetypes
from settings import settings
from io import StringIO, BytesIO


class S3:
    def __init__(
        self,
        required_buckets: Sequence[str] = settings.AWS_BUCKETS,
        aws_access_key_id: str = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key: str = settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
        aws_host=settings.AWS_HOST,
        aws_use_ssl=settings.AWS_USE_SSL,
    ):
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.s3client = session.client(
            service_name="s3",
            endpoint_url=aws_host,
            use_ssl=aws_use_ssl,
        )
        self._required_buckets = required_buckets
        # create any non-existing buckets
        for bucket in required_buckets:
            try:
                self.s3client.head_bucket(Bucket=bucket)
            except botocore.exceptions.ClientError:
                self.create_bucket(bucketname=bucket)
        buckets = self.s3client.list_buckets()
        req = set(required_buckets)
        existing = {bucket["Name"] for bucket in buckets["Buckets"]}
        if not (req <= existing):
            raise ConnectionError(
                f"Required buckets are {required_buckets}, but found {existing}"
            )

    def get_url(self, fileid: str, bucket="ats-data") -> None:
        try:
            self.s3client.head_object(Bucket=bucket, Key=fileid)

            (mime, encoding) = mimetypes.guess_type(fileid, strict=True)
            if not mime:
                return self.s3client.generate_presigned_url(
                    "get_object",
                    ExpiresIn=600,
                    Params={"Bucket": bucket, "Key": fileid},
                )
            else:
                return self.s3client.generate_presigned_url(
                    "get_object",
                    ExpiresIn=600,
                    Params={
                        "Bucket": bucket,
                        "Key": fileid,
                        "ResponseContentType": mime,
                    },
                )
        except botocore.exceptions.ClientError:
            raise FileNotFoundError("File not found")

    def download_file(self, file: BytesIO | StringIO, fileid: str, bucket: str) -> None:
        try:
            self.s3client.head_object(Bucket=bucket, Key=fileid)
            self.s3client.download_fileobj(bucket, fileid, file)
            file.seek(0)
        except botocore.exceptions.ClientError:
            raise FileNotFoundError("File not found")

    def upload_file(self, file: BytesIO | StringIO, fileid: str, bucket: str) -> None:
        self.s3client.upload_fileobj(file, bucket, fileid)

    def create_bucket(self, bucketname: str) -> None:
        try:
            self.s3client.create_bucket(Bucket=bucketname)
        except Exception as ex:
            pass
            # logging.info(ex)
    
    @property
    def required_buckets(self) -> Sequence[str]:
        return self._required_buckets
