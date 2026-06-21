import os, boto3
ep=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
s3=boto3.client("s3", endpoint_url=ep,
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"])
bucket=os.environ["R2_BUCKET_NAME"]
prefix="national-bank-of-belgium/subsets/national-bank-of-belgium-df-exttradebecom/"
keys=[]
tok=None
while True:
    kw=dict(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
    if tok: kw["ContinuationToken"]=tok
    r=s3.list_objects_v2(**kw)
    keys+=[o["Key"] for o in r.get("Contents",[])]
    if r.get("IsTruncated"): tok=r["NextContinuationToken"]
    else: break
import sys
total=sum(1 for _ in keys)
print(f"objects under prefix: {total}")
for k in keys[:8]: print("  ", k)
# safety: ensure every key starts with the exact prefix
assert all(k.startswith(prefix) for k in keys), "prefix mismatch!"
if "--delete" in sys.argv and keys:
    for i in range(0,len(keys),1000):
        batch=[{"Key":k} for k in keys[i:i+1000]]
        s3.delete_objects(Bucket=bucket, Delete={"Objects":batch})
    print(f"DELETED {len(keys)} objects")
