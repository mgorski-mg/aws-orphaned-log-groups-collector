# AWS Orphaned Log Groups Collector
Orphaned Log Groups Collector deletes log groups not associated with any resources in the AWS Account.

## Why is it helpful?
Deleting AWS resources even using CloudFormation does not delete the corresponding CloudWatch Log Groups what cause unnecessary costs.

### Supported services
- AWS Lambda
- Amazon API Gateway

## Getting Started
### Prerequisites
- Python 3.7+
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Deployment
To deploy Orphaned Log Group Collector edit deploy.bat file and change
- \<stack-name> - new stack name 
- \<s3-bucket-name> - s3 bucket name for code and template file needed for deployment of the AWS Lambda
- \<s3-bucket-prefix> - logical folder for the code and template file

Then run the file.

### Input Lambda Event
```json
{
    "view_only": true,
    "regions": ["us-west-1", "..."]
}
```
### Default values
- view_only: true
- regions: all regions

# **It is strongly recommended to use view_only mode first!!**

## Scheduler
Orphaned Log Groups Collector by default is scheduled every first day of the month. 

The schedule can be changed by overriding `SchedulerCronParameter`.

The scheduler can be disabled using `SchedulerEnabledParameter`.