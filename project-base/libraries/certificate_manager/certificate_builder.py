from aws_cdk import (
    aws_certificatemanager as cert,
    core as cdk
)

from aws_cdk.core import Tags

class CertificateBuilder(cdk.Construct):

    @property
    def certificate(self):
        return self.__certificate

    def __init__(self, scope: cdk.Construct, id: str, domain: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__domain_name = domain        
        self.__create_certificate()
    
    def __create_certificate(self):      
        self.__certificate = cert.Certificate(
            self, self.__id,                      
            domain_name = self.__domain_name,
            validation = cert.CertificateValidation.from_dns()
        )
    
        Tags.of(self.__certificate).add('Name', self.__id)

class CertificateFromArnBuilder(cdk.Construct):

    @property
    def certificate(self):
        return self.__certificate

    def __init__(self, scope: cdk.Construct, id: str, arn: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__arn = arn
        self.__create_certificate()
    
    def __create_certificate(self):      
        self.__certificate = cert.Certificate.from_certificate_arn(
            self, self.__id,
            certificate_arn = self.__arn
        )
        

        