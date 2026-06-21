import io
import pandas as pd
from subsets_utils import get
RAW="https://github.com/StackExchange/Survey/raw/refs/heads/main/packages/archive"
def read_csv(content,**kw):
    for enc in ("utf-8-sig","cp1252","latin-1"):
        try: return pd.read_csv(io.BytesIO(content),dtype=str,encoding=enc,**kw)
        except UnicodeDecodeError: pass
for year in ("2011","2014","2016"):
    c=get(f"{RAW}/{year}/results.csv",timeout=(10.0,300.0)); c.raise_for_status()
    df=read_csv(c.content,low_memory=False)
    unnamed=[col for col in df.columns if str(col).startswith("Unnamed:")]
    # which unnamed are droppable: <=1 distinct non-null value
    drop=[col for col in unnamed if df[col].nunique(dropna=True)<=1]
    keep_unnamed=[col for col in unnamed if col not in drop]
    print(f"{year}: total={df.shape[1]} unnamed={len(unnamed)} droppable={len(drop)} kept_unnamed={keep_unnamed[:3]}")
    if keep_unnamed:
        col=keep_unnamed[0]; print(f"   kept e.g. {col!r} distinct={df[col].nunique()} sample={df[col].dropna().unique()[:3]}")
