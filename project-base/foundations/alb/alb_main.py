from aws_cdk import (
    aws_elasticloadbalancingv2 as alb,
    core
)

from aws_cdk.aws_ec2 import (
    IVpc,
    ISecurityGroup, 
)

from aws_cdk.aws_elasticloadbalancingv2 import (
    IApplicationTargetGroup,
    IApplicationListener,
    ListenerCertificate,    
    ListenerCondition,
)

from aws_cdk.core import Tags

class ALBMain(core.Construct):

    @property
    def alb_main(self):
        return self.__alb_main
    
    @property
    def https_listener(self) -> IApplicationListener:
        return self.__https_listener

    def __init__(self, scope: core.Construct, id: str, vpc: IVpc, sg: ISecurityGroup, cert_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__vpc = vpc
        self.__sg = sg
        self.__cert_arn = cert_arn
        self.__create_alb()
        self.__create_http_listener()
        self.__create_https_listener()

    def __create_alb(self):       
        self.__alb_main = alb.ApplicationLoadBalancer(
            self, self.__id,
            vpc = self.__vpc,
            security_group = self.__sg,
            load_balancer_name = self.__id,            
            internet_facing = True
        )
        Tags.of(self.__alb_main).add('Name', self.__id)        

    def __create_http_listener(self):       
        self.__alb_main.add_listener(
            self.__id + '-http-lst',
            protocol = alb.ApplicationProtocol.HTTP,
            port = 80,
            default_action = alb.ListenerAction.redirect(
                permanent = True,
                port = '443',
                protocol = 'HTTPS'             
            )         
        )        
    
    def __create_https_listener(self):
        self.__https_listener = self.__alb_main.add_listener(
            self.__id + '-https-lst',
            protocol = alb.ApplicationProtocol.HTTPS,
            port = 443,
            default_action = alb.ListenerAction.fixed_response(
                status_code = 503,
                content_type = 'text/plain',
                message_body = 'AWS ALB - Path unknown.'
            ),
            certificates = [ListenerCertificate(
                certificate_arn = self.__cert_arn
            )]
        )                

    def add_https_listener_role(self, id: str, target_group: IApplicationTargetGroup, host_headers: str, priority: int):      
        self.__https_listener.add_target_groups(
            id = id,
            target_groups = [target_group],
            conditions = [
                ListenerCondition.host_headers([host_headers])
            ],
            priority = priority
        )        