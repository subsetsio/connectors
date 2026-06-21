import io, zipfile
import nodes.instituto_de_estad_sticas_de_puerto_rico as m
m._ensure_http()
res = m._api("package_show", id="mortalidad-infantil-cohortes")["resources"][0]
print("res:", res.get("name"), res.get("format"), res.get("url")[-50:])
c = m._download_bytes(res["url"])
z = zipfile.ZipFile(io.BytesIO(c))
for n in z.namelist():
    if n.lower().endswith(".txt"):
        data = z.read(n)[:300]
        print(f"\n--- {n} ({z.getinfo(n).file_size}B) ---")
        print(repr(data[:250]))
