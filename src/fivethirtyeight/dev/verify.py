import sys; sys.path.insert(0,'src')
import nodes.fivethirtyeight as m
from subsets_utils import get
for path in ["biopics/biopics.csv", "next-bechdel/nextBechdel_crewGender.csv", "star-wars-survey/StarWars.csv", "airline-safety/airline-safety.csv"]:
    c = get("https://raw.githubusercontent.com/fivethirtyeight/data/master/"+path, timeout=(10.0,120.0)).content
    t = m._parse_csv(c)
    # ensure every string cell is valid utf-8 (encode round-trip)
    bad=0
    for col in t.columns:
        if col.type == __import__('pyarrow').string():
            for v in col.to_pylist():
                if v is not None:
                    v.encode('utf-8')
    print(f"OK {path}: rows={t.num_rows} cols={t.num_columns}")
