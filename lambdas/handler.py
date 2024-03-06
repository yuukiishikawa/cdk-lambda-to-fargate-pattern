import boto3
import os, json
from botocore.exceptions import ClientError

def run_direct_event(event, context):    
    runner =  FargateWrapper(event)
    runner.run()
    
class FargateWrapper:

    def __init__(self, params):
        from botocore.config import Config
        conf = Config(read_timeout=900, retries={'max_attempts': 0})
        self.params = json.dumps(params)
        self.region = os.getenv('region')
        self.client = boto3.client('lambda',
                                   region_name=self.region,
                                   config=conf)

    def __run_ecs_task(self, app_name):
        try:
            client = boto3.client('ecs')
            print(self.params)
            print("os.getenv('ECS_TASK_NAME')")
            print(os.getenv('ECS_TASK_NAME'))
            print(os.getenv('ECS_SUBNET_IDS'))
            response = client.run_task(
                # cluster='audio-summarizer-cluster',  # name of the cluster
                cluster=os.getenv('ECS_CLUSTER_NAME'),
                launchType='FARGATE',
                #taskDefinition=os.getenv('ECS_TASK_DEFINITION_NAME'),
                taskDefinition="FargateApiStackfargateapitaskdef25358AF7",
                count=1,
                platformVersion='LATEST',
                networkConfiguration={
                    'awsvpcConfiguration': {
                        'subnets': os.environ["ECS_SUBNET_IDS"].split(","),
                        'assignPublicIp': 'ENABLED'
                    }
                },
                overrides={
                    'containerOverrides': [{
                        'name': os.getenv('ECS_TASK_NAME'),
                        'command': [
                            "python", "-m", "EcsTask",  "--app", app_name, "--params", self.params
                        ],
                        'environment': [{
                            'name': 'OPENAI_API_KEY',
                            'value': os.environ['OPEN_AI_API_KEY']
                        }, {
                            'name': 'DYNAMODB_TABLE_RESOURCE',
                            'value': os.environ['DYNAMODB_TABLE_RESOURCE']
                        }               # add more parameters as needed
                        ]
                    }]
                },
            )
            print(str(response))
            return str(response)
        except ClientError as error:
            print(f"ClientError: {str(error)}")
            return None
        
    def run(self):
        app_name = os.getenv('ECS_APP_NAME')
        return self.__run_ecs_task(app_name)