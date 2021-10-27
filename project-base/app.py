#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from project_base.project_base_stack import ProjectBaseStack

env_params = {
    'account' : '575125170529', 
    'region' : 'us-east-1'
}

app = cdk.App()
ProjectBaseStack(app, "ProjectBaseStack", env = env_params)
app.synth()
