from subsets_utils.delta import subsets_uri
from subsets_utils import delta as D
from deltalake import DeltaTable
name="federal-reserve-bank-of-new-york-soma-holdings"
uri=subsets_uri(name)
opts=D.backend.deltalake_options(uri)
dt=DeltaTable(uri, storage_options=opts)
print("uri:",uri)
print("version:",dt.version())
print("schema cols:",[f.name for f in dt.schema().fields])
print("n_files:",len(dt.file_uris()))
