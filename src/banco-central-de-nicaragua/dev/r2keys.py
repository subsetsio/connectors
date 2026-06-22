import os, boto3, collections
acct=os.environ["R2_ACCOUNT_ID"]
s3=boto3.client("s3",endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],region_name="auto")
b=os.environ["R2_BUCKET_NAME"]
paginator=s3.get_paginator("list_objects_v2")
seg=collections.Counter()
sample=[]
n=0
for page in paginator.paginate(Bucket=b,Prefix="banco-central-de-nicaragua/"):
    for o in page.get("Contents",[]):
        n+=1
        k=o["Key"]
        parts=k.split("/")
        seg[parts[1] if len(parts)>1 else k]+=1
        if len(sample)<8 and "subset" in k: sample.append(k)
print("total keys",n)
print("second-segment counts:",dict(seg))
print("subset samples:")
for s in sample: print("  ",s)
