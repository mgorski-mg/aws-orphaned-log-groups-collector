# AWS Lambda Orphaned Log Groups Collector
Orphaned Log Groups Collector deletes AWS Lambda related log groups not associated with any AWS Lambda in the AWS Account.

Available on the [AWS Serverless Application Repository](https://aws.amazon.com/serverless) - [orphaned-log-groups-collector](https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/create/app?applicationId=arn:aws:serverlessrepo:eu-west-1:275418140668:applications/orphaned-log-groups-collector)

## Why is it helpful?
Deleting AWS resources even using CloudFormation does not delete the corresponding CloudWatch Log Groups what cause unnecessary costs.

### Supported services
- AWS Lambda

## Getting Started
### Prerequisites
- Python 3.9+
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Deployment
To deploy Orphaned Log Group Collector edit deploy.bat file and change
- \<stack-name> - new stack name 
- \<s3-bucket-name> - s3 bucket name for code and template file needed for deployment of the AWS Lambda
- \<s3-bucket-prefix> - logical folder for the code and template file

Then run the Lambda.

### Input Lambda Event
```json
{
    "dry_run": true,
    "regions": ["us-west-1", "..."]
}
```
### Default values
- dry_run: true
- regions: all regions

# **It is strongly recommended to use dry_run mode first!!**

## Scheduler
Orphaned Log Groups Collector by default is scheduled every first day of the month. 

The schedule can be changed by overriding `SchedulerCronParameter`.

The scheduler can be disabled using `SchedulerEnabledParameter`.
