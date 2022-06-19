import base64
from datetime import date
from google.cloud import storage

def upload_blob(bucket_name, contents, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

def email(content):
    import os
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email
    from python_http_client.exceptions import BadRequestsError

    try:
        sg_client = SendGridAPIClient(os.environ['EMAIL_API_KEY'])
    except Exception as e:
        print("Environment Variable {} not found!".format(e))
        exit()
    
    message = Mail(
        to_emails = ["lekesh.kumar@searce.com"],
        from_email = Email(email='lekeshkumar2000@gmail.com', name="Your name"),
        subject = "Pubsub Message {}".format(date.today()),
        plain_text_content = content
    )

    try:
        response = sg_client.send(message)
        print("Email sent")
        return f"email.status_code={response.status_code}"

    except BadRequestsError as e:
        print(e.body)
        exit()

def hello_pubsub(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    obj_name = "pubsub_message_{}".format(date.today())
    upload_blob("lekesh_test", pubsub_message, obj_name)
    email(pubsub_message)
