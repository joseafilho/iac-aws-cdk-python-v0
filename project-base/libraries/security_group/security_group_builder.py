from aws_cdk import (
    aws_ec2 as ec2,    
    core
)

from aws_cdk.aws_ec2 import (
    IVpc,
    ISecurityGroup
)

from aws_cdk.core import Tags

class SecurityGroupBuilder(core.Construct):

    @property
    def sg(self) -> ISecurityGroup:
        return self.__sg
    
    def __init__(self, scope: core.Construct, id: str, vpc: IVpc, sg_description: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__id = id
        self.__vpc = vpc        
        self.__sg_description = sg_description        
        self.__create_sg()    

    def __create_sg(self):      
        self.__sg = ec2.SecurityGroup(
            self, 
            self.__id, 
            vpc = self.__vpc, 
            security_group_name = self.__id, 
            description = self.__sg_description
        )                                   
        
        Tags.of(self.__sg).add('Name', self.__id)

    def add_role(self, port: int, rule_description: str, source_ip: str = '127.0.0.1/32', sg_parent: ISecurityGroup = None):
        if sg_parent:
            self.__sg.connections.allow_from(sg_parent, ec2.Port.tcp(port), rule_description)                        
        else:      
            self.__sg.add_ingress_rule(ec2.Peer.ipv4(source_ip), ec2.Port.tcp(port), rule_description)

        