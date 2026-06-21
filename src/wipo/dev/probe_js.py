import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import re
from subsets_utils import get

for u in ['https://www3.wipo.int/ipstats/main.649b62b91ba3b94e.js',
          'https://www3.wipo.int/ipstats/184.4739a4f1ffa3d285.js',
          'https://www3.wipo.int/ipstats/886.8bf92d0fcec5105f.js']:
    r = get(u, timeout=(10, 120))
    t = r.text
    name = u.split('/')[-1]
    for kw in ['table-result', 'downloadCsv', 'pmh-search']:
        idxs = [m.start() for m in re.finditer(re.escape(kw), t)]
        if idxs:
            print(f'\n### {name}  kw={kw}  hits={len(idxs)}')
            for i in idxs[:4]:
                print(repr(t[max(0, i - 250):i + 150]))
                print('  ...')
