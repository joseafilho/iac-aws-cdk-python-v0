from aws_cdk import (
    aws_ec2 as ec2,    
    core as cdk
)

from aws_cdk.core import (
    SecretValue, 
    Tags
)

import aws_cdk.aws_logs as logs
import aws_cdk.aws_rds as rds
from aws_cdk.aws_ec2 import ISecurityGroup
from aws_cdk.aws_ec2 import IVpc
from libraries.security_group.security_group_builder import SecurityGroupBuilder

class BeerRDSResources(cdk.Construct):   
    
    def __init__(self, scope: cdk.Construct, id: str, vpc: IVpc, sg_beer_backend: ISecurityGroup, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__vpc = vpc
        self.__sg_beer_backend = sg_beer_backend

        self.__create_sg()
        self.__create_rds_instance()
    
    def __create_sg(self):        
        self.__sg_rds = SecurityGroupBuilder(
            self, 'beer-rds-postgres-sg',
            vpc = self.__vpc,
            sg_description = 'Access RDS Postgres'
        )        

        self.__sg_rds.add_role(
            port = 5432,
            sg_parent = self.__sg_beer_backend,
            rule_description = 'Beer backend.'
        )       

    def __create_rds_instance(self):

        instance_name = 'beer-db'
        
        instance_type = ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE4_GRAVITON,
            ec2.InstanceSize.SMALL
        )

        instance = rds.DatabaseInstance(self, instance_name,
            engine = rds.DatabaseInstanceEngine.postgres(
                version = rds.PostgresEngineVersion.VER_12_7
            ),            
            instance_type = instance_type,
            credentials = rds.Credentials.from_password(
                username = 'postgres_admin',
                password = SecretValue.plain_text('db_password')
            ),
            vpc = self.__vpc,            
            vpc_subnets = {
                'subnet_type': ec2.SubnetType.PUBLIC
            },
            security_groups = [self.__sg_rds.sg],
            allocated_storage = 50,
            max_allocated_storage = 1000,
            publicly_accessible = False,
            instance_identifier = instance_name,
            backup_retention = cdk.Duration.days(7),
            monitoring_interval = cdk.Duration.seconds(60),
            enable_performance_insights = True,
            cloudwatch_logs_exports = ['postgresql'],
            cloudwatch_logs_retention = logs.RetentionDays.ONE_WEEK,
            deletion_protection = True,
            auto_minor_version_upgrade = False
        )

        Tags.of(instance).add('Name', instance_name)