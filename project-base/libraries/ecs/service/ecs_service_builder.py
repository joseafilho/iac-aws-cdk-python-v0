from aws_cdk import (    
    aws_ecs as ecs,
    aws_ec2 as ec2,    
    core
)

from aws_cdk.aws_ecs import (
    ITaskDefinition,
    ICluster,    
)

from aws_cdk.core import (
    Tags,
    Duration
)

from aws_cdk.aws_ec2 import (
    ISecurityGroup
)

class ECSServiceBuilder(core.Construct):

    @property
    def service(self):
        return self.__service

    def __init__(self, scope: core.Construct, id: str, task_definition: ITaskDefinition, cluster: ICluster, sg: ISecurityGroup, desired_count: int, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__id = id                
        self.__task_definition = task_definition
        self.__cluster = cluster
        self.__sg = sg
        self.__desired_count = desired_count
        self.__create_service()

    def __create_service(self):       
        self.__service = ecs.FargateService(
            self, self.__id,
            task_definition = self.__task_definition,
            cluster = self.__cluster,
            service_name = self.__id,
            desired_count = self.__desired_count,
            health_check_grace_period = Duration.seconds(360),            
            security_groups = [self.__sg],
            assign_public_ip = True
        )

        Tags.of(self.__service).add('Name', self.__id)