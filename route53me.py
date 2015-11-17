import boto3
import requests
import re
import time

# Replace below with correct hosted zone id, host name, and desired TTL
hostedZoneId = 'ZK8XMWWB*****'
hostName = 'host.dyn.example.com'
ttl = 60

# Any ip lookup service that returns just the ip address as text
ipifyEndpoint = 'https://api.ipify.org'

validIpRegex = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

thisPublicIp = requests.get(ipifyEndpoint).text

validIpPattern = re.compile(validIpRegex)

validIpMatch = validIpPattern.match(thisPublicIp)

if validIpMatch == None:
  # Not a valid ip address
  exit('Invalid IP Address: ' + thisPulbicIp)

route53 = boto3.client('route53')

route53.change_resource_record_sets(
    HostedZoneId = hostedZoneId,
    ChangeBatch = {
        'Comment' : 'Last updated by route53me.py at ' % time.gmtime(),
        'Changes' : [
            {
                'Action' : 'UPSERT',
                'ResourceRecordSet' : 
                {
                    'Name' : hostName,
                    'Type' : 'A',
                    'TTL' : ttl,
                    'ResourceRecords' :
                    [
                        {
                            'Value' : thisPublicIp
                        },
                    ]
                }
            },
        ]
    }
)

print ('Updated to ' + thisPublicIp)


