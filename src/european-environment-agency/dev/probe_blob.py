from subsets_utils import get
import io, zipfile
url="https://dis2datalake.blob.core.windows.net/discodata/airqualitydataflows/v1r1/models.zip"
r=get(url, timeout=(10,180))
print("status",r.status_code,"ct",r.headers.get("content-type"),"len",len(r.content))
try:
    z=zipfile.ZipFile(io.BytesIO(r.content))
    print("names:", z.namelist())
    n=z.namelist()[0]
    data=z.read(n)
    print("member",n,"bytes",len(data))
    print("head:", data[:400])
except Exception as e:
    print("not a zip / err:", type(e).__name__, e)
    print("head bytes:", r.content[:200])
