from subsets_utils import get

# 1) Does the production client reach the .tab files?
for u in [
    "https://bioconductor.org/packages/stats/bioc/bioc_pkg_stats.tab",
    "https://bioconductor.org/packages/stats/data-experiment/experiment_pkg_stats.tab",
]:
    r = get(u, timeout=(10, 60))
    print("TAB", r.status_code, u, "len", len(r.content))

# 2) VIEWS reachable + parse shape
r = get("https://bioconductor.org/packages/release/bioc/VIEWS", timeout=(10, 120))
print("VIEWS", r.status_code, "bytes", len(r.content))
text = r.text
pkgs = sum(1 for ln in text.splitlines() if ln.startswith("Package:"))
print("software package count", pkgs)
