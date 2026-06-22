import os, boto3
acct=os.environ["R2_ACCOUNT_ID"]
s3=boto3.client("s3",endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],region_name="auto")
b=os.environ["R2_BUCKET_NAME"]
pfx="banco-central-de-nicaragua/data/subsets/"
paginator=s3.get_paginator("list_objects_v2")
names=set()
for page in paginator.paginate(Bucket=b,Prefix=pfx,Delimiter="/"):
    for cp in page.get("CommonPrefixes",[]):
        names.add(cp["Prefix"].split("subsets/")[1].rstrip("/"))
dotted=sorted(n for n in names if "." in n)
clean=sorted(n for n in names if "." not in n)
print("total",len(names),"dotted orphans",len(dotted),"clean",len(clean))
for n in dotted[:6]: print("  orphan:",n)
open("dev/orphans.txt","w").write("\n".join(dotted))
