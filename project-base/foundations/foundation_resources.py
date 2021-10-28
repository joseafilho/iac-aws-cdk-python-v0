from aws_cdk import (        
    core as cdk
)

from aws_cdk.aws_ec2 import (    
    IVpc,
    ISecurityGroup
)

from aws_cdk.aws_elasticloadbalancingv2 import IApplicationListener
from aws_cdk.aws_certificatemanager import ICertificate
from foundations.alb.alb_main import ALBMain
from libraries.certificate_manager.certificate_builder import CertificateBuilder, CertificateFromArnBuilder
from libraries.utils.global_consts import Domains
from libraries.security_group.security_group_builder import SecurityGroupBuilder
from libraries.s3.bucket_private_builder import BucketPrivateBuilder

class FoundationResources(cdk.Construct):    

    @property
    def sg_alb(self) -> ISecurityGroup:
        return self.__sg_alb.sg

    @property
    def alb_https_listener(self) -> IApplicationListener:
        return self.__alb_main.https_listener

    @property
    def cert_company_com_br(self) -> ICertificate:
        return self.__cert_company_com_br.certificate
    
    def __init__(self, scope: cdk.Construct, id: str, vpc: IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__vpc = vpc        
        self.__create_sg()
        self.__create_certificates()        
        self.__create_alb()          

    def __create_sg(self):
        self.__sg_alb = SecurityGroupBuilder(
            self, 'company-alb-sg',
            vpc = self.__vpc,
            sg_description = 'SG dedicated to access via ALB.'
        )

        self.__sg_alb.add_role(
            port = 80,
            source_ip = '0.0.0.0/0',
            rule_description = 'HTTP.'
        )

        self.__sg_alb.add_role(
            port = 443,
            source_ip = '0.0.0.0/0',
            rule_description = 'HTTPS.'
        )
    
    def __create_certificates(self):
        self.__cert_company_com_br = CertificateBuilder(
            self, 'company-com-br-certificate',
            domain = f'*.{Domains.DOMAIN_COMPANY}'
        )        

    def __create_alb(self):
        self.__alb_main = ALBMain(
            self, 'alb-main',
            vpc = self.__vpc,
            sg = self.__sg_alb.sg,
            cert_arn = self.__cert_company_com_br.certificate.certificate_arn
        )