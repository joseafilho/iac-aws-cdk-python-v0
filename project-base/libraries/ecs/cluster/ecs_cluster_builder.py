from aws_cdk import (    
    aws_ecs as ecs,    
    core
)

from aws_cdk.aws_ec2 import (
    IVpc
)

from aws_cdk.core import Tags

class ECSClusterBuilder(core.Construct):

    @property
    def cluster(self) -> ecs.ICluster:
        return self.__cluster

    def __init__(self, scope: core.Construct, id: str, vpc: IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__id = id 
        self.__vpc = vpc
        self.__create_cluster()

    def __create_cluster(self):
        self.__cluster = ecs.Cluster(
            self, self.__id,
            cluster_name = self.__id,
            vpc = self.__vpc
        )
                        
        Tags.of(self.__cluster).add('Name', self.__id)
