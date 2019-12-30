import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class LambdaEngine:
    def __init__(self, region):
        self.__services = self.__get_lambda_resources(region)

    def is_orphan(self, log_group_name):
        if log_group_name.startswith('/aws/lambda/'):
            function_name = log_group_name.split("/")[3]

            if function_name in self.__services:
                return 0
            else:
                return 1
        else:
            return 0

    @staticmethod
    def __get_lambda_resources(region):
        services = []

        try:
            paginator = boto3.client('lambda', region_name=region).get_paginator('list_functions')
            for response in paginator.paginate():
                for function in response.get('Functions'):
                    services.append(function['FunctionName'])
        except EndpointConnectionError as e:
            print(e)
        except ClientError as e:
            print(e)

        return services
