import subsets_utils as su
import json

BASE = "https://hgk.tjj.beijing.gov.cn/query/queryres/queryreport/"
HTML = "https://hgk.tjj.beijing.gov.cn/query/queryReport/queryReportAction"

# Test report
report = "60Y-1-03-N"
subject = "0100"
dept = "071"
sortType = "01"
freqType = "C_YY"

def show(name, resp):
    print("===", name, resp.status_code, resp.headers.get("content-type"))
    t = resp.text
    print("len", len(t))
    print(t[:1500])
    print()

# 1. queryDataSortType
r = su.post(BASE + "QueryReportAction!queryDataSortType", timeout=(10,60))
show("queryDataSortType", r)

# 2. queryRptTimeFreqMask
data = {
  "reportDataKeyDTO.reportNumber": report,
  "reportDataKeyDTO.reportVersion": "",
  "reportDataKeyDTO.queryType": "",
  "reportDataKeyDTO.usageType": "01",
  "reportDataKeyDTO.dataSortTypeCode": sortType,
}
r = su.post(BASE + "QueryReportAction!queryRptTimeFreqMask", data=data, timeout=(10,60))
show("queryRptTimeFreqMask", r)
