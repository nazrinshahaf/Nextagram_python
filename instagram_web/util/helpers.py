import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET,S3_LOCATION
from app import app
from models import *
from flask_login import current_user
from flask import redirect, url_for, render_template
from datetime import *
from flask_login import current_user

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def upload_file_to_s3(file, bucket_name, acl="public-read"):

    now = datetime.now()
    date_string = now.strftime("%Y%m%d%H%M%S")
    file.filename = f"{date_string}{current_user.username}{file.filename}"

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    return file.filename 
    
    


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

