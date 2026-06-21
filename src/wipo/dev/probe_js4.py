import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import re
from subsets_utils import get

bundles = {
    'main': 'https://www3.wipo.int/ipstats/main.649b62b91ba3b94e.js',
    '184': 'https://www3.wipo.int/ipstats/184.4739a4f1ffa3d285.js',
}
texts = {k: get(v, timeout=(10, 120)).text for k, v in bundles.items()}

for name, t in texts.items():
    for m in re.finditer(r'SelValues', t):
        i = m.start()
        snip = t[max(0, i - 40):i + 10]
        # only print unique-ish param-name contexts
        print(f"[{name}] ...{snip}...")
