import sys,importlib; sys.path.insert(0,"src")
import subsets_utils as su
CAP={}
su.save_raw_parquet=lambda t,a:CAP.__setitem__(a,t)
mod=importlib.import_module("nodes.ppac"); mod.save_raw_parquet=su.save_raw_parquet
mod.fetch_refinery_capacity("ppac-infrastructure/installed-refinery-capacity")
df=CAP["ppac-infrastructure/installed-refinery-capacity"].to_pandas()
print(df['as_of'].unique(), "| companies:", df['company'].nunique(), "| sample:", df.iloc[0].to_dict())
