import os
os.environ["CI"]="1"
from subsets_utils import config
from subsets_utils.delta import subsets_uri
from subsets_utils import delta as D
from deltalake import DeltaTable
print("is_cloud:", config.is_cloud())
name="federal-reserve-bank-of-new-york-soma-holdings"
uri=subsets_uri(name)
print("uri:",uri)
opts=D.backend.deltalake_options(uri)
dt=DeltaTable(uri, storage_options=opts)
print("version:",dt.version())
print("cols:",[f.name for f in dt.schema().fields])
