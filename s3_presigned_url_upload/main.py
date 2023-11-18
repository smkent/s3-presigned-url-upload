import argparse
import functools
import sys
from configparser import RawConfigParser
from pathlib import Path
from pprint import pprint
from typing import Dict

import boto3
import botocore
import requests


class S3PresignedURLMain:
    ACTIONS = {"upload", "download"}

    @functools.cached_property
    def args(self) -> argparse.Namespace:
        ap = argparse.ArgumentParser()
        ap.add_argument(
            "action",
            choices=self.ACTIONS,
            help="Action to perform",
            default="download",
        )
        ap.add_argument(
            "-b",
            "--bucket",
            dest="bucket_name",
            metavar="bucket-name",
            help="Bucket name",
        )
        ap.add_argument(
            "-f",
            "--file-path",
            "--object-name",
            dest="object_name",
            metavar="file-path",
            help="S3 destination object name (file path)",
        )
        ap.add_argument(
            "-l",
            "--local-file",
            dest="local_file",
            metavar="file",
            help="Local source file to upload",
        )
        ap.add_argument(
            "-e",
            "--expires",
            dest="expires",
            metavar="seconds",
            default=30,
            help="URL expiration in seconds",
        )
        return ap.parse_args()

    @functools.cached_property
    def s3_client(self) -> botocore.client.BaseClient:
        def aws_config_from_s3cfg() -> Dict[str, str]:
            conf = RawConfigParser()
            conf.read(str(Path.home() / ".s3cfg"))
            return dict(conf["default"])

        conf = aws_config_from_s3cfg()
        print("Creating S3 client")
        return boto3.client(
            "s3",
            aws_access_key_id=conf["access_key"],
            aws_secret_access_key=conf["secret_key"],
            endpoint_url=conf["host_base"],
        )

    @functools.cached_property
    def bucket_name(self) -> str:
        try:
            self.s3_client.head_bucket(Bucket=self.args.bucket_name)
        except botocore.exceptions.ClientError:
            print(f"Error: Bucket {self.args.bucket_name} does not exist")
            sys.exit(1)
        return str(self.args.bucket_name)

    @functools.cached_property
    def object_name(self) -> str:
        return str(self.args.object_name.lstrip("/"))

    def run(self) -> None:
        # Invoke selected action method
        getattr(self, f"action_{self.args.action}")()

    def action_download(self) -> None:
        print("Creating signed download URL")
        url = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": self.object_name},
            ExpiresIn=self.args.expires,
        )
        print(url)

    def action_upload(self) -> None:
        print("Creating signed upload parameters")
        upload_info = self.s3_client.generate_presigned_post(
            self.bucket_name, self.object_name, ExpiresIn=self.args.expires
        )
        pprint(upload_info)
        if not self.args.local_file:
            return

        print(
            f"Uploading {self.args.local_file}"
            f" to {self.bucket_name} as {self.object_name}"
        )
        with open(self.args.local_file, "rb") as f:
            upload_response = requests.post(
                upload_info["url"],
                data=upload_info["fields"],
                files={"file": (self.object_name, f)},
                timeout=30,
            )
        print("Upload response: ", upload_response)
        if not upload_response.ok:
            print("Response headers:")
            for k, v in upload_response.headers.items():
                print(f"    {k}: {v}")
            print("Response body:")
            print("----")
            print(upload_response.text)


def main() -> None:
    S3PresignedURLMain().run()
