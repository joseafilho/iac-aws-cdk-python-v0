from aws_cdk import (    
    aws_ecr as ecr,    
    core
)

from aws_cdk.core import (
    Tags,
    Duration
)

class ECRBuilder(core.Construct):

    @property
    def repository(self):
        return self.__repository

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.__id = id
        self.__create_life_cycle()
        self.__create_ecr()        

    def __create_life_cycle(self):
        self.__life_cycle = ecr.LifecycleRule(
            description = 'Remove untagged images.',            
            tag_status = ecr.TagStatus.UNTAGGED,
            max_image_age = Duration.days(1)
        )

    def __create_ecr(self):
        self.__repository = ecr.Repository(
            self, self.__id,
            repository_name = self.__id,
            lifecycle_rules = [self.__life_cycle]
        )
                   
        Tags.of(self.__repository).add('Name', self.__id)