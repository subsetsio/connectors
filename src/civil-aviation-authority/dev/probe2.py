import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re
from subsets_utils import get
def html(u):
    r=get(u, timeout=(10,120)); r.raise_for_status(); return r.text
# airline landing
al="https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airlines/uk-airline-data/"
yrs=sorted(set(re.findall(r'/uk-airline-data-(\d{4})/', html(al))))
print("AIRLINE years:", yrs)
# punctuality landing - try a couple of candidate landing urls
for pl in [
  "https://www.caa.co.uk/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics/",
  "https://www.caa.co.uk/data-and-analysis/uk-aviation-market/flight-punctuality/uk-flight-punctuality-statistics",
]:
    try:
        h=html(pl)
        yrs=sorted(set(re.findall(r'/uk-flight-punctuality-statistics/(\d{4})/', h)))
        print("PUNCT landing OK", pl, "years:", yrs)
        break
    except Exception as e:
        print("PUNCT fail", pl, type(e).__name__, e)
