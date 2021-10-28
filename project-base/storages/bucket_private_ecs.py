from aws_cdk import (        
    core as cdk,
    aws_iam as iam
)

from libraries.s3.bucket_private_builder import BucketPrivateBuilder

class BucketPrivateECS(cdk.Construct):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__bucket_uploads = BucketPrivateBuilder(
            self, 'company-uploads-bk'
        )

        bucket_uploads_arn = self.__bucket_uploads.bucket.bucket_arn + '/*'

        self.__bucket_uploads.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                principals = [
                    iam.ServicePrincipal('ecs-tasks.amazonaws.com')

                ],
                actions = ['*'],
                resources = [bucket_uploads_arn]
            )
        )