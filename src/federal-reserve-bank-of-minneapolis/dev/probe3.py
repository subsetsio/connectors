import io
import pandas as pd
from subsets_utils import get
for url in [
  "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-",
]:
    r = get(url, timeout=(10.0,60.0)); r.raise_for_status()
    tables = pd.read_html(io.StringIO(r.text))
    big = max(tables, key=lambda x: x.shape[0])
    print(url.rsplit('/',1)[-1], "ntables", len(tables), "shape", big.shape, "cols", list(big.columns))
    print(big.head(2).to_string()); print(big.tail(2).to_string())
