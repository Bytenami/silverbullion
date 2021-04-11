import json
import requests
import os
import boto3
import datetime as dt

s3 = boto3.resource(
    's3',
    region_name = 'us-east-2',
    aws_access_key_id = os.environ.get("aws_access_key_id_s3"),
    aws_secret_access_key = os.environ.get("aws_secret_access_key_s3")

)

def lambda_handler(event, context):
    # TODO implement
    url = "https://www.silverbullion.com.sg/Product/Detail/Gold_1_kg_ABC_bar"
    data = requests.get(url)
    fnam = f"silver_bullion_gold_{dt.datetime.now()}.html"
    s3.Object("bn-silverbullion", fnam).put(Body=data.text)
    return {
        'statusCode': 200,
        'headers': "blah",
        'body': len(data.text),
        'size': len(data.text)
    }
