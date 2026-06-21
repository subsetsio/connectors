import os, sys, json, boto3
ep=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"
s3=boto3.client("s3", endpoint_url=ep,
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"])
bucket=os.environ["R2_BUCKET_NAME"]
base="national-bank-of-belgium/data/subsets/"

# current valid table names from the persisted transform snapshot
cur=json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/national-bank-of-belgium/assets/transform/current.json"))
valid=set(v["id"].replace("-transform","") for v in cur.values())

# list all subset dirs
dirs=[]
tok=None
while True:
    kw=dict(Bucket=bucket, Prefix=base, Delimiter="/", MaxKeys=1000)
    if tok: kw["ContinuationToken"]=tok
    r=s3.list_objects_v2(**kw)
    dirs+=[p["Prefix"] for p in r.get("CommonPrefixes",[])]
    if r.get("IsTruncated"): tok=r["NextContinuationToken"]
    else: break

stale=[]
for d in dirs:
    name=d[len(base):].rstrip("/")
    if name not in valid:
        stale.append((name,d))
print(f"total dirs={len(dirs)} valid_current={len(valid)} stale={len(stale)}")
for name,d in stale: print("  STALE:", name)

def del_prefix(prefix):
    n=0; tok=None
    while True:
        kw=dict(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
        if tok: kw["ContinuationToken"]=tok
        r=s3.list_objects_v2(**kw)
        objs=[{"Key":o["Key"]} for o in r.get("Contents",[])]
        if objs:
            s3.delete_objects(Bucket=bucket, Delete={"Objects":objs}); n+=len(objs)
        if r.get("IsTruncated"): tok=r["NextContinuationToken"]
        else: break
    return n

if "--delete" in sys.argv:
    for name,d in stale:
        # safety: only ever delete under the subsets base, and only known trade mains
        assert d.startswith(base)
        c=del_prefix(d)
        print(f"  deleted {c} objects under {name}")
