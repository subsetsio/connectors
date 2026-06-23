import json, pandas as pd, warnings
warnings.simplefilter("ignore")
mapping=json.load(open("dev/mapping.json"))
def show(fn):
    path="dev/files/"+fn
    print("\n==================", fn)
    if fn.lower().endswith(".csv"):
        df=pd.read_csv(path, header=None, dtype=str, nrows=6)
        print("CSV shape(first6):", df.shape)
        print(df.to_string(max_cols=12))
    else:
        xl=pd.ExcelFile(path)
        print("sheets:", xl.sheet_names)
        df=pd.read_excel(path, sheet_name=0, header=None, nrows=6, dtype=str)
        print("sheet0 shape(first6):", df.shape)
        print(df.to_string(max_cols=12))
import sys
names=sys.argv[1:] or list(mapping.values())
for fn in names:
    try: show(fn)
    except Exception as e: print("ERR", fn, type(e).__name__, e)
