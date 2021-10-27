from aws_cdk.core import IConstruct
from aws_cdk.core import Tags

class DefaultTags():

    @staticmethod
    def apply(target: IConstruct):            
        Tags.of(target).add('Enterprise', 'FireCloud Services') # You company name.
        Tags.of(target).add('Environment', 'production') # Ex.: development, staging, production
        Tags.of(target).add('IaC', 'true') # Differ of another resource created manually.