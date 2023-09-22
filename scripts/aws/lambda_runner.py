#!/usr/bin/env python3
import concurrent.futures
import json

try:
    import boto3
except ImportError:
    print('This script requires the Boto3 module.')
    exit()

lambda_client = boto3.client('lambda')

def invoke_lambda(payload):
    response = lambda_client.invoke(
        FunctionName='FUNK-0',
        InvocationType='RequestResponse',
        Payload=bytes(json.dumps(payload).encode('utf-8'))
    )
    response_payload = json.loads(response['Payload'].read())
    return response_payload

payloads = [{'key': f'value_{i}'} for i in range(100)]

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(invoke_lambda, payloads))

for result in results:
    print(result)