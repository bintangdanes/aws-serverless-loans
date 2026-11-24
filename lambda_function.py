import json
import os
import boto3
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'ganti-dengan-nama-bucket')
FILE_KEY = 'loans_data.json'

def read_data():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        return json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        return []

def write_data(data):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=FILE_KEY,
        Body=json.dumps(data, indent=2),
        ContentType='application/json'
    )

def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod', 'GET')
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body) if body else {}

    loans = read_data()

    if method == 'GET':
        return response(200, {"message": "Success", "data": loans})

    elif method == 'POST':
        new_item = {
            "loan_id": body.get("loan_id", f"LN-{len(loans)+1:03d}"),
            "item_name": body.get("item_name", "Multimeter"),
            "borrower_name": body.get("borrower_name", "Mahasiswa"),
            "status": "BORROWED",
            "loan_date": datetime.utcnow().strftime("%Y-%m-%d")
        }
        loans.append(new_item)
        write_data(loans)
        return response(201, {"message": "Created", "data": new_item})

    elif method == 'PUT':
        loan_id = body.get("loan_id")
        for item in loans:
            if item["loan_id"] == loan_id:
                item["status"] = body.get("status", "RETURNED")
                write_data(loans)
                return response(200, {"message": "Updated", "data": item})
        return response(404, {"message": "Loan ID not found"})

    elif method == 'DELETE':
        loan_id = body.get("loan_id")
        updated_loans = [item for item in loans if item["loan_id"] != loan_id]
        write_data(updated_loans)
        return response(200, {"message": f"Deleted {loan_id}"})

    return response(400, {"message": "Unsupported method"})

def response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_dict)
    }
