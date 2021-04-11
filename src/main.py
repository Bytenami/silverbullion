import json
import requests

def lambda_handler(event, context):
    # TODO implement
    url = "https://www.silverbullion.com.sg/Product/Detail/Gold_1_kg_ABC_bar"
    data = requests.get(url)
    return {
        'statusCode': 200,
        'headers': "blah",
        'body': len(data.text),
        'size': len(data.text)
    }
