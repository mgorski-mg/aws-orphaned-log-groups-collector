import boto3
from botocore.exceptions import ClientError, EndpointConnectionError


class RdsEngine:
    def __init__(self, region):
        self.__services = self.__get_rds_resources(region)

    def is_orphan(self, log_group_name):
        if log_group_name.startswith('/aws/rds/cluster/'):
            cluster_name = log_group_name.split("/")[4]

            if cluster_name in self.__services:
                return 0
            else:
                return 1
        else:
            return 0

    @staticmethod
    def __get_rds_resources(region):
        services = []

        try:
            paginator = boto3.client('rds', region_name=region).get_paginator('describe_db_clusters')
            for response in paginator.paginate():
                for cluster in response.get('DBClusters'):
                    services.append(cluster['DBClusterIdentifier'])
        except EndpointConnectionError as e:
            print(e)
        except ClientError as e:
            print(e)

        return services
