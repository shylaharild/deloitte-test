import json
import random

def website(event, context):
    random_number = random.randint(1,100)
    body = {
        "message": "The random number is " + str(random_number)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
