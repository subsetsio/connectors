from subsets_utils import get
import io, zipfile, csv

# 1) Inspect the bulk ZIP central directory + one CSV's header/rows per indicator.
url = "https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip"
r = get(url, timeout=(10, 300))
print("zip status", r.status_code, "bytes", len(r.content))
zf = zipfile.ZipFile(io.BytesIO(r.content))
names = zf.namelist()
print("num files", len(names))
for n in names[:50]:
    print("  ", n, zf.getinfo(n).file_size)
