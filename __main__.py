"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3
from pulumi_aws import iam
from pulumi import Output
import json

config = {
    "data_engs": ["varokas", "non", "shadow"],
    "data_ops": ["ops1"]
}
bucket = 'varokas-pulumi-demo-data'
project_tags = {"Project": "Bedrock"}

# Bucket
bucket_example = s3.Bucket('varokas-pulumi-demo-data', bucket=bucket, tags=project_tags)

# Group 
data_engs_group = iam.Group("data_engs", path="/data_engs/")
data_ops_group = iam.Group("data_ops", path="/data_ops/")

# Users 
data_engs = [ iam.User(u) for u in config["data_engs"] ]
data_engs_membership = iam.GroupMembership("data_engs", 
                                           users=[u.name for u in data_engs],
                                           group=data_engs_group.name)
data_ops = [ iam.User(u) for u in config["data_ops"] ]
data_ops_membership = iam.GroupMembership("data_ops", 
                                           users=[u.name for u in data_ops],
                                           group=data_ops_group.name)

# Policies
bucket_readonly_all = iam.Policy("s3_read_only",
    path="/s3/",
    description="S3 ReadOnly",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [ {
            "Effect":"Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource":"*"
        }, {
            "Effect": "Allow",
            "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
            "Resource": f"arn:aws:s3:::{bucket}"
        }, {
            "Action": ["s3:GetObject"],
            "Effect": "Allow",
            "Resource": [
                f"arn:aws:s3:::{bucket}/*",
            ],
        }],
    }))

bucket_readwrite_path = iam.Policy("s3_datadump_writing",
    path="/s3/",
    description="S3 Write to datadump",
    policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [ {
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectVersion",
                "s3:GetObjectVersionAcl",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutObjectVersionAcl"
            ],
            "Effect": "Allow",
            "Resource": [
                f"arn:aws:s3:::{bucket}/datadump/*",
            ],
        }],
    }))

iam.GroupPolicyAttachment("bucket_readonly_data_eng",
    group=data_engs_group.name,
    policy_arn=bucket_readonly_all.arn)

iam.GroupPolicyAttachment("bucket_readonly_data_ops",
    group=data_ops_group.name,
    policy_arn=bucket_readonly_all.arn)
iam.GroupPolicyAttachment("bucket_write_datadump_data_ops",
    group=data_ops_group.name,
    policy_arn=bucket_readwrite_path.arn)

# Permission
pulumi.export('bucket_name', bucket_example.id)