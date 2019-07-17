import os
from os.path import expanduser
import configparser
import boto3

def read_credentials_from_config_section(section_name):
    # parsing ~/.aws/credentials but it's just as easy to parse ~/.boto
    aws_credentials_path = os.path.join(expanduser("~"), '.aws', 'credentials')
    c = configparser.ConfigParser()
    c.read(aws_credentials_path)
    return c.get(section_name, 'aws_access_key_id'), c.get(section_name, 'aws_secret_access_key')



def get_bucket():
    # k, s = read_credentials_from_config_section('speech2text')
    # session = boto3.Session(
    # aws_access_key_id=k,
    # aws_secret_access_key=s,
    # region_name='eu-west-1'
    # )
    session = boto3.Session()
    s3 = session.resource('s3')
    my_bucket = s3.Bucket('chatbot-speech-to-text')
    return my_bucket

bucket = get_bucket()


def get_file(file,directory):
    filepath = '{}/{}'.format(directory,file)
    bucket.download_file(file,filepath)
    return filepath