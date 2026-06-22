import subsets_utils as su, json
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
report="60Y-1-03-N"; subject="0100"; sortType="01"; freqType="C_YY"; dept="071"
v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2"
su.get(v, timeout=(10,60))
d={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.reportVersion":"","reportDataKeyDTO.queryType":"","reportDataKeyDTO.usageType":"01","reportDataKeyDTO.dataSortTypeCode":sortType}
fm=su.post(NS+"queryRptTimeFreqMask", data=d, timeout=(10,60)); print("freqMask", fm.text)
yr="2013"
key={"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.departmentCode":dept,
     "reportDataKeyDTO.collectFrequenceMask":yr,"reportDataKeyDTO.collectFrequenceTypeCode":freqType,
     "reportDataKeyDTO.usageType":"01","reportDataKeyDTO.objectType":"04",
     "reportDataKeyDTO.objectCode":subject,"reportDataKeyDTO.reportVersion":"","reportDataKeyDTO.queryType":""}
uh=su.post(NS+"updateReportHtml", data=key, timeout=(10,120)); print("updateReportHtml", uh.status_code, "len", len(uh.text))
rd=su.post(NS+"queryReportData", data=key, timeout=(10,120)); print("queryReportData", rd.status_code, "len", len(rd.text), "head", rd.text[:100])
open("dev/sample_template.html","w").write(uh.text)
open("dev/sample_data.json","w").write(rd.text)
