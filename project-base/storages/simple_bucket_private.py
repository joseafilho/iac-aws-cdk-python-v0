from aws_cdk import (        
    core as cdk
)

from libraries.s3.bucket_private_builder import BucketPrivateBuilder

class SimpleBucketPrivate(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        BucketPrivateBuilder(
            self, id
        )