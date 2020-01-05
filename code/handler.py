import json
import boto3
from engines.lambda_engine import LambdaEngine
from engines.apigateway_engine import ApigatewayEngine


def lambda_handler(event, context):
    view_only = get_view_only_parameter(event)
    regions = get_regions_parameter(event)

    for region in regions:
        print('REGION: {}'.format(region))
        logs_client = boto3.client('logs', region_name=region)
        orphaned_log_groups = find_orphans(region, logs_client)
        delete_log_groups(orphaned_log_groups, logs_client, region, view_only)


def find_orphans(region, logs_client):
    lambda_engine = LambdaEngine(region)
    apigateway_engine = ApigatewayEngine(region)

    orphaned_log_groups = []

    paginator = logs_client.get_paginator('describe_log_groups')
    for response in paginator.paginate():
        for log_group in response.get('logGroups'):
            log_group_name = log_group['logGroupName']
            if lambda_engine.is_orphan(log_group_name) or apigateway_engine.is_orphan(log_group_name):
                orphaned_log_groups.append(log_group)

    return orphaned_log_groups


def delete_log_groups(orphaned_log_groups, logs_client, region, view_only):
    if view_only:
        print(json.dumps(orphaned_log_groups))
    else:
        for log_group in orphaned_log_groups:
            logs_client.delete_log_group(logGroupName=log_group['logGroupName'])

    print('There were {} orphaned log groups in {}.\n'.format(len(orphaned_log_groups), region))


def get_view_only_parameter(event):
    if 'view_only' not in event:
        return 1
    else:
        return event['view_only']


def get_regions_parameter(event):
    regions = []

    if 'regions' in event and type(event['regions']) == list:
        regions = event['regions']

    if not regions:
        region_response = boto3.client('ec2').describe_regions()
        regions = [region['RegionName'] for region in region_response['Regions']]

    return regions
