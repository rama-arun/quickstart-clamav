import boto3
import os
import sys
import subprocess
import uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        version = record['s3']['object']['versionId']
        file_name = '/tmp/' + key.split('/')[-1]

        s3_client.download_file(bucket, key, file_name)

        # scan_cmd = 'ls -al ' + file_name
        # sp = subprocess.Popen(scan_cmd,
        #                       shell=True,
        #                       stdout=subprocess.PIPE,
        #                       stderr=subprocess.PIPE,
        #                       universal_newlines=True)

        # out, err = sp.communicate()
        # return_code = sp.wait()

        # print("Return Code: " + str(return_code))
        # print("Standard out: \n", out)
        # print("Sending notification with scan results: \n", err)

        scan_cmd = 'clamscan --quiet ' + file_name
        sp = subprocess.Popen(scan_cmd,
                              shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True)

        out, err = sp.communicate()

        # * clamscan return values (documented from man clamscan)
        # *  0 : No virus found.
        # *  1 : Virus(es) found.
        # * 40: Unknown option passed.
        # * 50: Database initialization error.
        # * 52: Not supported file type.
        # * 53: Can't open directory.
        # * 54: Can't open file. (ofm)
        # * 55: Error reading file. (ofm)
        # * 56: Can't stat input file / directory.
        # * 57: Can't get absolute path name of current working directory.
        # * 58: I/O error, please check your file system.
        # * 62: Can't initialize logger.
        # * 63: Can't create temporary files/directories (check permissions).
        # * 64: Can't write to temporary directory (please specify another one).
        # * 70: Can't allocate memory (calloc).
        # * 71: Can't allocate memory (malloc).

        return_code = sp.wait()

        if return_code == 0:
            print("Clean File. No Action!")
        else:
            print("Return Code: " + str(return_code))
            print("Standard out: \n", out)

            preferredAction = os.environ.get('preferredAction')
            if preferredAction == "Delete":
                delete_response = s3_client.delete_object(Bucket=bucket,
                                        Key=key,
                                        # VersionId=version
                                        )
                print("Attempted deleting the tainted object. Result: " + str(delete_response))
            else:
                tag_response = s3_client.put_object_tagging(
                    Bucket=bucket,
                    Key=key,
                    # versionId=version,
                    Tagging={'TagSet': [
                        {
                            'Key': 'Tainted',
                            'Value': 'Yes'
                        },
                    ]})

                print("Attempted tagging the tainted object. Result: " +
                      str(tag_response))

            print("Sending notification with scan results: \n", err)
            snsTopicARN = os.environ.get('snsTopic')
            sns_client = boto3.client('sns')
            sns_client.publish(
                TopicArn=snsTopicARN,
                Subject='Malware detected in your S3 bucket',
                Message=
                'Malware detected in your S3 bucket. Bucket: ' +
                bucket + ': key: ' + key + ': version: ' + version + 
                '. Infected object has been deleted')
