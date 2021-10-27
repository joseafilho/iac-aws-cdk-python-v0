from aws_cdk import (
    aws_s3 as s3,
    core as cdk
)

class BucketPrivateBuilder(cdk.Construct):

    @property
    def bucket(self) -> s3.Bucket:
        return self.__bucket

    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__create_bucket()        
    
    def __create_bucket(self):
        self.__bucket = s3.Bucket(
            self, self.__id,
            bucket_name = self.__id,
            block_public_access = s3.BlockPublicAccess(
                block_public_acls = True, 
                block_public_policy = True, 
                ignore_public_acls = True,
                restrict_public_buckets = True
            )
        )