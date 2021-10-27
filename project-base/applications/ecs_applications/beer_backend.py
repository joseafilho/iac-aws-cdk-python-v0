from aws_cdk import (
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    core as cdk,
    aws_iam as iam
)

from aws_cdk.aws_ec2 import (
    IVpc,
    ISecurityGroup,    
)

from aws_cdk.aws_elasticloadbalancingv2 import (
    IApplicationListener
)

from libraries.utils.global_consts import Domains
from aws_cdk.core import Duration
from aws_cdk.aws_certificatemanager import ICertificate
from libraries.ecs.cluster.ecs_cluster_builder import ECSClusterBuilder
from libraries.security_group.security_group_builder import SecurityGroupBuilder
from libraries.ecs.ecr.ecr_builder import ECRBuilder
from libraries.ecs.task_definition.fargate_task_definition_builder import FargateTaskDefinitionBuilder
from libraries.ecs.service.ecs_service_builder import ECSServiceBuilder
from libraries.utils.alb_utils import ALBUtils
from libraries.s3.bk_private_builder import BucketPrivateBuilder

class BeerBackendResources(cdk.Construct):

    @property
    def sg_beer_backend(self) -> ISecurityGroup:
        return self.__sg_service.sg
    
    def __init__(self, scope: cdk.Construct, id: str, vpc: IVpc, sg_alb: ISecurityGroup, alb_listener: IApplicationListener, certificate: ICertificate, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.__vpc = vpc
        self.__sg_alb = sg_alb
        self.__alb_listener = alb_listener

        # Consts
        self.__NODE_EXPRESS_PORT = 3000

        self.__create_backend()

    def __create_backend(self):     
        self.__create_sg()   
        self.__create_repository_images()        
        self.__create_cluster()
        self.__create_task_definition()
        self.__create_service()
        self.__create_target_listener()

    def __create_sg(self):
        self.__sg_service = SecurityGroupBuilder(
            self, 'beer-sg-ecs',
            vpc = self.__vpc,
            sg_description = 'SG dedicated to api beer.'            
        )

        self.__sg_service.add_role(
            port = self.__NODE_EXPRESS_PORT,
            rule_description = 'Node Express port.',
            sg_parent = self.__sg_alb
        )        

    def __create_repository_images(self):        
        self.__ecr_beer = ECRBuilder(
            self, 'beer-ecr'
        )

    def __create_cluster(self):
        self.__ecs_cluster = ECSClusterBuilder(self, f'beer-cluster', self.__vpc)

    def __create_task_definition(self):
        self.__task_definition = FargateTaskDefinitionBuilder(
            self, f'beer-task-definition',
            repository = self.__ecr_beer.repository,
            cpu = 512,
            memory_limit = 1024,
            port_mapping = self.__NODE_EXPRESS_PORT,
            tag_image = 'latest'
        )

    def __create_service(self):       
        self.__beer_service = ECSServiceBuilder(
            self, f'beer-service',            
            task_definition = self.__task_definition.definition,
            cluster = self.__ecs_cluster.cluster,
            sg = self.__sg_service.sg,
            desired_count = 1
        )

    def __create_target_listener(self):
        ALBUtils.AddTargetInListener(
            id = f'beer-ecs-service-tg',
            alb_listener = self.__alb_listener,
            target = self.__beer_service.service,            
            port = self.__NODE_EXPRESS_PORT,
            priority = 1,
            health_check_path = '/ping',
            host_header = f'beer-api.{Domains.DOMAIN_COMPANY}'
        )