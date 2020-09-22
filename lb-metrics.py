import datetime
import boto3
from botocore.config import Config
import sys

if len(sys.argv) < 2:
    print("provide atleast alb/elb name in parameter")
    exit()

# my_config = Config(
#     region_name = 'us-west-2',
#     signature_version = 'v4',
#     retries = {
#         'max_attempts': 10,
#         'mode': 'standard'
#     }
# )

cw = boto3.client('cloudwatch')

data_points = cw.get_metric_statistics(
    Namespace='AWS/ApplicationELB',
    MetricName='RequestCount',
    Dimensions= [
                {
                    'Name': 'LoadBalancer',
                    'Value': str(sys.argv[1])
                }
            ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=60),
    EndTime=datetime.datetime.utcnow(),
    Period=60,
    Statistics=[
        'Sum',
    ],
    Unit='Count'
)

data_len = range(len(data_points['Datapoints']))
add_up = 0
for i in data_len:
    add_up += int(data_points['Datapoints'][i]['Sum'])

if add_up > 0:
    print ("Application ALB named " + str(sys.argv[1]) + " has traffic and request count is " + str(add_up))
else:
    print ("Application ALB named " + str(sys.argv[1]) + " has no traffic")

if len(sys.argv) > 2:
    classic_data_points = cw.get_metric_statistics(
        Namespace='AWS/ELB',
        MetricName='RequestCount',
        Dimensions= [
                    {
                        'Name': 'LoadBalancerName',
                        'Value': str(sys.argv[2])
                    }
                ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=240),
        EndTime=datetime.datetime.utcnow(),
        Period=60,
        Statistics=[
            'Sum',
        ],
        Unit='Count'
    )

    classic_add_up = 0
    for i in range(len(classic_data_points['Datapoints'])):
        classic_add_up += int(data_points['Datapoints'][i]['Sum'])

    if classic_add_up > 0: 
        print ("Classic ELB named " + str(sys.argv[2]) + " has traffic and request count is " + str(classic_add_up))
    else:
        print ("Classic ELB named " + str(sys.argv[2]) + " has no traffic")
