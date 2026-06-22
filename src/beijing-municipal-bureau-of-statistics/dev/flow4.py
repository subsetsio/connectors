import subsets_utils as su, json
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
report="60Y-1-03-N"; subject="0100"; sortType="01"; freqType="C_YY"; dept="071"
v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2"
su.get(v, timeout=(10,60))
# freqMask
fm=su.post(NS+"queryRptTimeFreqMask", data={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.usageType":"01","reportDataKeyDTO.dataSortTypeCode":sortType}, timeout=(10,60))
print("freqMask", fm.text)
# collectDataVersion
cv=su.post(NS+"queryReportCollectDataVersion", data={"reportDataKeyDTO.collectFrequenceMask":"2013","reportDataKeyDTO.departmentCode":dept,"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.collectFrequenceTypeCode":freqType}, timeout=(10,60))
print("collectDataVersion", cv.status_code, repr(cv.text))
# data with full payload
key={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.departmentCode":dept,
 "reportDataKeyDTO.collectFrequenceMask":"2013","reportDataKeyDTO.collectDataVersion":"1",
 "reportDataKeyDTO.collectFrequenceTypeCode":freqType,"reportDataKeyDTO.usageType":"01",
 "reportDataKeyDTO.objectType":"04","reportDataKeyDTO.objectCode":subject,
 "reportDataKeyDTO.reportVersion":"201301"}
rd=su.post(NS+"queryReportData", data=key, timeout=(10,120))
print("queryReportData", rd.status_code, "len", len(rd.text))
js=json.loads(rd.text)
print("n DSID blocks", len(js))
print("block0 keys", list(js[0].keys()))
print("DSID", js[0]["DSID"], "n rows", len(js[0]["data"]))
print("row0", json.dumps(js[0]["data"][0], ensure_ascii=False)[:400])
open("dev/sample_data.json","w").write(rd.text)
