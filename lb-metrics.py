import datetime
import boto3
from botocore.config import Config

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
                    'Value': 'app/vault-alb/54072ae09b85d482'
                }
            ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=120),
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

print(add_up)



classic_data_points = cw.get_metric_statistics(
    Namespace='AWS/ELB',
    MetricName='RequestCount',
    Dimensions= [
                {
                    'Name': 'LoadBalancerName',
                    'Value': 'classic-vault'
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

print (classic_data_points)

# now = datetime.datetime.utcnow()    
# twoHourAgo = datetime.datetime.utcnow() - datetime.timedelta(minutes=120)

# print("Current Time =", now)
# print ("two hour ago =", twoHourAgo)

# response = cw.get_metric_data(
#     MetricDataQueries=[
#         {
#             'Id': 'requestCountAlb',
#             'MetricStat': {
#                 'Metric': {
#                     'Namespace': 'AWS/ApplicationELB',
#                     'MetricName': 'RequestCount',
#                     'Dimensions': [
#                         {
#                             'Name': 'LoadBalancer',
#                             'Value': 'app/vault-alb/54072ae09b85d482'
#                         }
#                     ]
#                 },
#                 'Period': 60,
#                 'Stat': 'Sum',
#                 'Unit': 'Count'
#             },
#             'Label': 'vault-alb RequestCount',
#         },
#     ],
#     StartTime=twoHourAgo,
#     EndTime=now
# )

#print (response)

