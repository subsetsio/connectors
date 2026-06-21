import sys; sys.path.insert(0, "src")
import subsets_utils as su
def hit(slug, var="TAVG"):
    u=f"https://data.berkeleyearth.org/auto/Regional/{var}/Text/{slug}-{var}-Trend.txt"
    r=su.get(u, headers={"Range":"bytes=0-0"}, timeout=(10,60))
    return r.status_code
tricky=["united-states","south-korea","north-korea","russia","russian-federation",
        "democratic-republic-of-the-congo","republic-of-the-congo","cote-d-ivoire",
        "ivory-coast","united-arab-emirates","saudi-arabia","czech-republic","czechia",
        "turkey","turkiye","myanmar","burma","vietnam","viet-nam","laos","syria",
        "bosnia-and-herzegovina","trinidad-and-tobago","papua-new-guinea","sri-lanka",
        "new-zealand","united-kingdom","south-africa","el-salvador","costa-rica",
        "dominican-republic","puerto-rico"]
print("=== regional country slugs ===")
for s in tricky:
    print(f"{hit(s):>3} {s}")
# continents
print("=== continents ===")
for s in ["asia","europe","africa","north-america","south-america","oceania","antarctica","australia"]:
    print(f"{hit(s):>3} {s}")
# global S3 products
print("=== global S3 products ===")
base="https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/"
for f in ["Land_and_Ocean_complete.txt","Complete_TAVG_complete.txt","Complete_TMAX_complete.txt","Complete_TMIN_complete.txt"]:
    r=su.get(base+f, headers={"Range":"bytes=0-0"}, timeout=(10,60))
    print(f"{r.status_code:>3} {f}")
