import logging
import boto3
from botocore.exceptions import ClientError
from master_config import aws_config
import traceback

#
# with open("../aws/config.yaml", 'r') as stream:
#     config = yaml.safe_load(stream)

bucket = aws_config['s3_storage_bucket']

def upload_file_to_s3_base(file_name, storage_folder, file_extension, uuid_name, content_type):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name

    object_name = '{}/{}{}'.format(aws_config[storage_folder], uuid_name, file_extension)

    object_url = "{}/{}".format(aws_config["s3_service_url"], object_name)

    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        print(file_name, bucket, object_name)
        with open(file_name, 'rb') as f:
            response = s3_client.upload_fileobj(f, bucket, object_name, ExtraArgs={'ContentType': content_type})

    except ClientError as e:
        logging.error(e)
        return False
    print("Uploaded", response)
    return object_name, object_url

def download_file_from_s3_base(object_name, file_name):

    s3 = boto3.client('s3')
    s3.download_file(bucket, object_name, file_name)



def make_file_public(object_name):
    s3 = boto3.resource('s3')

    try:
        object_acl = s3.ObjectAcl(bucket, object_name)
        object_acl.put(ACL="public-read")
        return True
    except:
        print(traceback.print_exc())
        return False

