import re
from subsets_utils import get

# 1. discover current filenames from the WPI download page
page = get("https://eaindustry.nic.in/download_data_1112.asp", timeout=(10,60)).text
print("=== monthly_index links on download_data_1112.asp ===")
for m in sorted(set(re.findall(r'[\w/]*monthly_index_\d{6}\.xls', page)))[-5:]:
    print(m)
print("=== other index hrefs ===")
for m in sorted(set(re.findall(r'href="([^"]+\.xls[x]?)"', page, re.I)))[:40]:
    print(m)
