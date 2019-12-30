import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class ApigatewayEngine:
    def __init__(self, region):
        self.__apigatewayClient = boto3.client('apigateway', region_name=region)
        self.__services = self.__get_apigateway_resources(self.__apigatewayClient)

    def is_orphan(self, log_group_name):
        if log_group_name.startswith('/aws/apigateway/') or log_group_name.startswith('API-Gateway-Execution-Logs'):
            if log_group_name.startswith('/aws/apigateway/'):
                api_id = log_group_name.split("/")[3]
                stage_name = log_group_name.split("/")[4]
            else:
                api_id = log_group_name.split("/")[0].split("_")[1]
                stage_name = log_group_name.split("/")[1]

            if api_id in self.__services:
                stages = self.__apigatewayClient.get_stages(restApiId=api_id).get('item')
                stage_names = list(map(lambda s: s['stageName'], stages))
                if stage_name in stage_names:
                    return 0
            return 1
        else:
            return 0

    @staticmethod
    def __get_apigateway_resources(apigateway_client):
        services = []

        try:
            paginator = apigateway_client.get_paginator('get_rest_apis')
            for response in paginator.paginate():
                for apigateway in response.get('items'):
                    services.append(apigateway['id'])
        except EndpointConnectionError as e:
            print(e)
        except ClientError as e:
            print(e)

        return services
