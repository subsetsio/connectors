import os, boto3
acct=os.environ["R2_ACCOUNT_ID"]
s3=boto3.client("s3",endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],region_name="auto")
b=os.environ["R2_BUCKET_NAME"]
orphans=[x for x in open("dev/orphans.txt").read().splitlines() if x.strip()]
assert all("." in n for n in orphans), "safety: only dotted orphans"
paginator=s3.get_paginator("list_objects_v2")
total_del=0
for name in orphans:
    pfx=f"banco-central-de-nicaragua/data/subsets/{name}/"
    keys=[]
    for page in paginator.paginate(Bucket=b,Prefix=pfx):
        for o in page.get("Contents",[]): keys.append({"Key":o["Key"]})
    for i in range(0,len(keys),1000):
        s3.delete_objects(Bucket=b,Delete={"Objects":keys[i:i+1000]})
    total_del+=len(keys)
print("deleted",total_del,"objects across",len(orphans),"orphan subsets")
