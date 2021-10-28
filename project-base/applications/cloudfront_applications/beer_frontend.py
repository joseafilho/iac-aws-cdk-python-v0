from aws_cdk import (
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    core as cdk
)

from aws_cdk.aws_ec2 import ISecurityGroup
from libraries.utils.global_consts import Domains
from aws_cdk.core import Duration
from aws_cdk.aws_certificatemanager import ICertificate
from libraries.s3.bucket_private_builder import BucketPrivateBuilder

class BeerFrontendResources(cdk.Construct):

    @property
    def sg_siprev(self) -> ISecurityGroup:
        return self.__sg_service.sg
    
    def __init__(self, scope: cdk.Construct, id: str, certificate: ICertificate, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.__certificate = certificate
        self.__create_frontend()

    def __create_frontend(self):        
        self.__create_bucket_origin()
        self.__create_distribution()        

    def __create_bucket_origin(self):        
        self.__bucket_origin = BucketPrivateBuilder(
            self, f'beer-frontend-bk'
        ).bucket


    def __create_distribution(self):                      
        error_response_403 = self.__create_error_reponse(http_status = 403)
        error_response_404 = self.__create_error_reponse(http_status = 404)
        
        cf.Distribution(
            self, f'beer-cf',
            domain_names = [f'beer.{Domains.DOMAIN_COMPANY}'],
            certificate = self.__certificate,
            default_root_object = 'index.html',
            error_responses = [error_response_403, error_response_404],
            default_behavior = cf.BehaviorOptions(
                origin = origins.S3Origin(self.__bucket_origin),
                viewer_protocol_policy = cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods = cf.AllowedMethods.ALLOW_ALL
            )
        )

    def __create_error_reponse(self, http_status: int):
        return cf.ErrorResponse(
            http_status = http_status,
            response_http_status = 200,
            response_page_path = '/index.html',
            ttl = Duration.seconds(300)
        )