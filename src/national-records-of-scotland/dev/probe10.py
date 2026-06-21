import sys; sys.path.insert(0,'src')
from nodes import national_records_of_scotland as M
ds=M.DATA_BASE+"household-type"
print("structure triple:", M._sparql(f'SELECT ?dsd WHERE {{ <{ds}> <http://purl.org/linked-data/cube#structure> ?dsd }}'))
print("obs predicates:")
for r in M._sparql(f'SELECT DISTINCT ?p WHERE {{ ?o <http://purl.org/linked-data/cube#dataSet> <{ds}> ; ?p ?v }}'):
    print("  ",r["p"])
