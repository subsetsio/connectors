import pandas as pd, sys
def peek(fn, nrows=12):
    print("\n========",fn)
    if fn.lower().endswith(".csv"):
        try:
            df=pd.read_csv("dev/files/"+fn, header=None, dtype=object, nrows=nrows, keep_default_na=False)
        except Exception as e:
            print("csv err",e); 
            for i,l in enumerate(open("dev/files/"+fn, encoding="utf-8", errors="replace")):
                if i>=nrows: break
                print(repr(l[:160]))
            return
        print(df.to_string(max_cols=10))
    else:
        xl=pd.ExcelFile("dev/files/"+fn); print("sheets:",xl.sheet_names)
        df=pd.read_excel("dev/files/"+fn, sheet_name=0, header=None, dtype=object, nrows=nrows)
        print(df.to_string(max_cols=10))
for fn in sys.argv[1:]:
    try: peek(fn)
    except Exception as e: print("ERR",fn,e)
