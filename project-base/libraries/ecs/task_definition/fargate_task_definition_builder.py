from aws_cdk import (    
    aws_ecs as ecs,    
    core
)

from aws_cdk.aws_ecr import IRepository
from aws_cdk.core import Tags
from aws_cdk.aws_logs import RetentionDays

class FargateTaskDefinitionBuilder(core.Construct):

    @property
    def definition(self) -> ecs.FargateTaskDefinition:
        return self.__task_definition

    def __init__(self, scope: core.Construct, id: str, cpu: int, memory_limit: int, port_mapping: int, repository: IRepository = None, image_name_docker_hub: str = '', tag_image: str = 'latest', **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__id = id
        self.__repository = repository
        self.__cpu = cpu
        self.__memory_limit = memory_limit
        self.__port_mapping = port_mapping
        self.__image_name_docker_hub = image_name_docker_hub
        self.__tag_image = tag_image        
        self.__create_task_definition()

    # TODO - Araujo, Marcelo - 06042021 - Pesquisar como criar a task definition com um nome passado por parametro.
    def __create_task_definition(self):
        self.__task_definition = ecs.FargateTaskDefinition(
            self, self.__id,            
            cpu = self.__cpu,
            memory_limit_mib = self.__memory_limit
        )

        if self.__repository:
            image_task = ecs.ContainerImage.from_ecr_repository(
                repository = self.__repository,
                tag = self.__tag_image
            )
        else:
            image_task = ecs.ContainerImage.from_registry(self.__image_name_docker_hub)

        self.__task_definition.add_container(
            self.__id + '-ctn',
            image = image_task,
            port_mappings = [
                ecs.PortMapping(
                    container_port = self.__port_mapping,
                    host_port = self.__port_mapping
                )
            ],
            logging = ecs.LogDriver.aws_logs(
                stream_prefix = 'ecs',
                log_retention = RetentionDays.THREE_DAYS
            )
        )

        Tags.of(self.__task_definition).add('Name', self.__id)