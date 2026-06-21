import os, boto3
ep=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
s3=boto3.client("s3", endpoint_url=ep,
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"])
bucket=os.environ["R2_BUCKET_NAME"]
base="national-bank-of-belgium/data/subsets/"
r=s3.list_objects_v2(Bucket=bucket, Prefix=base, Delimiter="/")
pre=[p["Prefix"] for p in r.get("CommonPrefixes",[])]
print("subset dirs:", len(pre))
for p in pre:
    if "exttrade" in p: print("  TRADE:", p)
