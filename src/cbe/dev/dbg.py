import io, re
from subsets_utils import get, configure_http
import openpyxl
from parser import parse_sheet, read_grid, _is_header_row, clean
configure_http(headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9"})
BASE="https://www.cbe.org.eg"
url="/-/media/project/cbe/listing/time-series/inflation/wpi-and-ppi/wpiandppi_monthly2020-2021_.xlsx"
r=get(BASE+url,timeout=(10,120))
wb=openpyxl.load_workbook(io.BytesIO(r.content),read_only=True,data_only=True)
ws=wb[wb.sheetnames[0]]
grid=read_grid(ws)
for i in range(4):
    print(i,"hdr?",_is_header_row(grid[i]),[clean(c) for c in grid[i][:5]])
rows=parse_sheet(grid,2020,2021,"monthly")
print("rows:",len(rows))
for x in rows[:3]: print(x)

# instrument
from parser import _is_header_row, is_num, _ffill, _period, clean
nrows=len(grid); ncols=max(len(r) for r in grid)
hdr_idx=[r for r in range(min(nrows,15)) if _is_header_row(grid[r])]
print("hdr_idx",hdr_idx)
last_hdr=max(hdr_idx); first_data=last_hdr+1
print("first_data",first_data)
valcols=set()
for r in range(first_data,nrows):
    for c in range(ncols):
        if c<len(grid[r]) and is_num(grid[r][c]): valcols.add(c)
print("valcols",sorted(valcols)[:15])
c0,c1=min(valcols),max(valcols)+1
filled=_ffill(grid,list(range(0,first_data)),c0,c1)
for c in range(c0,min(c1,c0+4)):
    toks=[filled[r].get(c) for r in range(0,first_data)]
    print("col",c,"toks",toks,"->",_period(toks,2020,2021,"monthly"))
