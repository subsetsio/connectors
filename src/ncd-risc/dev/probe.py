import io, zipfile, csv
from subsets_utils import get

url_csv = "https://www.ncdrisc.org/downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_standardised_world.csv"
url_page = "https://www.ncdrisc.org/data-downloads-diabetes.html"

for label, u in [("page", url_page), ("csv", url_csv)]:
    try:
        r = get(u, timeout=(10.0, 60.0))
        print(label, "status", r.status_code, "len", len(r.content), "ctype", r.headers.get("content-type"))
        if label == "csv":
            text = r.content.decode("utf-8", "replace")
            rows = list(csv.reader(io.StringIO(text)))
            print("  header:", rows[0])
            print("  row1:", rows[1])
            print("  nrows:", len(rows))
    except Exception as e:
        print(label, "ERR", type(e).__name__, repr(e)[:200])
