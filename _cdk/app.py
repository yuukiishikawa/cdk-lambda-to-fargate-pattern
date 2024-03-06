#!/usr/bin/env python3
import os

from aws_cdk import App, Environment, Stage
from constructs import Construct
from lib.fargate_api_stack import FargateApiStack
from lib.lambda_api_stack import LambdaApiStack

class MyStage(Stage):
    def __init__(self, scope: Construct, stack_id: str, stage_env):
        super().__init__(scope, stack_id, env=stage_env)


# export STAGE_NAME=dev
# export STAGE_NAME=prod
stage_name = os.getenv("STAGE_NAME")
app = App()

valid_stages = ["dev", "prod"]

if stage_name in valid_stages and stage_name == "dev":
    # Do something for dev stage
    env = Environment(region="ap-northeast-1")
    fargate_stack = FargateApiStack(app, "FargateApiStack", env=env, stage_name=stage_name)
    LambdaApiStack(app, "LambdaApiStack", env=env, stage_name=stage_name, fargate_stack=fargate_stack)

else:
    raise ValueError(f"Unknown stage: {stage_name}")

app.synth()
