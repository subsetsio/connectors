"""Baked entity->member-file map for the Census of India connector.

Generated from the NADA catalog: each accepted census table (entity) maps to
the stable Excel download URLs of its per-geography member files. URLs carry
persistent resource ids. Data, not logic.
"""

ENTITY_IDS = ["PC01_A01", "PC01_A02", "PC11_A01", "PC11_A02", "PC11_A11"]

ENTITY_FILES = {
 "PC01_A01": {
  "census_year": "2001",
  "table_code": "A-01",
  "title": "A-01: Number of villages, towns, households, population and area - 2001",
  "urls": [
   "https://censusindia.gov.in/nada/index.php/catalog/20028/download/23160/PC01_A01.xls"
  ]
 },
 "PC01_A02": {
  "census_year": "2001",
  "table_code": "A-02",
  "title": "A-02: Decadal variation in population since 1901 - 2001",
  "urls": [
   "https://censusindia.gov.in/nada/index.php/catalog/20032/download/23164/PC01_A02.xls"
  ]
 },
 "PC11_A01": {
  "census_year": "2011",
  "table_code": "A-01",
  "title": "A-01: Number of villages, towns, households, population and area (India, states/UTs, districts and Sub-districts) - 2011",
  "urls": [
   "https://censusindia.gov.in/nada/index.php/catalog/42526/download/46152/A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA.xlsx"
  ]
 },
 "PC11_A02": {
  "census_year": "2011",
  "table_code": "A-02",
  "title": "A-02: Decadal variation in population 1901-2011, India",
  "urls": [
   "https://censusindia.gov.in/nada/index.php/catalog/43333/download/47001/00%20A%202-India.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43334/download/47003/01%20A-2%20J%20%20K.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43335/download/47005/02%20A-2%20Himanchal%20pradesh.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43336/download/47007/03%20A-2%20Punjab.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43337/download/47009/04%20A-2%20Chandigarh.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43338/download/47011/05%20A-2%20Uttarakhand.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43339/download/47013/06%20A-2%20Haryana.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43340/download/47015/07A-2%20NCT%20Delhi.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43341/download/47017/08%20A-2%20Rajasthan.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43342/download/47019/09%20A-2Uttar%20Pradesh.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43343/download/47021/10%20A-2%20Bihar.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43344/download/47023/11%20A-2%20Sikkim.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43345/download/47025/12%20A-2%20Arunachal%20Pradesh.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43346/download/47027/13%20A-2%20Nagaland.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43347/download/47029/14%20A-2%20Manipur.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43348/download/47031/15%20A-2%20Mizoram.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43349/download/47033/16%20A-2%20Tirupura.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43350/download/47035/17%20A-2%20Meghalaya.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43351/download/47037/18%20A-2%20ASSAM.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43352/download/47039/19%20A-2%20West%20Bengal.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43353/download/47041/20%20A-2%20Jharkhand.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43354/download/47043/21%20A-2%20Odisha.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43355/download/47045/22%20A-2%20Chhattisgarh.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43356/download/47047/23%20A-2%20Madhya%20Pradesh.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43357/download/47049/24%20A-2%20Gujrat.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43358/download/47051/25%20A-2%20Daman%20%20Diu.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43359/download/47053/26%20A-2%20Dadra%20and%20Nagara%20haveli.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43360/download/47055/27%20A-2%20Maharastra.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43361/download/47057/28%20A-2%20Andhra%20Pradesh.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43362/download/47059/29%20A-2%20Karnataka.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43363/download/47061/30%20A-2%20Goa.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43364/download/47063/31%20A-2%20Lakshadweep.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43365/download/47065/32%20A-2%20Kerla%20Final.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43366/download/47067/33%20A-2%20Tamil%20Nadu.xls",
   "https://censusindia.gov.in/nada/index.php/catalog/43367/download/47069/34%20A-2%20PUDUCHERRY.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/43368/download/47071/35%20A-2%20Andaman%20%20Nicobar%20Islands.xlsx"
  ]
 },
 "PC11_A11": {
  "census_year": "2011",
  "table_code": "A-11",
  "title": "A-11: State primary census abstract (PCA) for individual scheduled tribes, Jammu and Kashmir - 2011",
  "urls": [
   "https://censusindia.gov.in/nada/index.php/catalog/42944/download/46612/ST-0100-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42945/download/46613/ST-0200-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42946/download/46614/ST-0500-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42947/download/46615/ST-0800-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42948/download/46616/ST-0900-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42949/download/46617/ST-1000-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42950/download/46618/ST-1100-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42951/download/46619/ST-1200-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42952/download/46620/ST-1300-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42953/download/46621/ST-1400-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42954/download/46622/ST-1500-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42955/download/46623/ST-1600-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42956/download/46624/ST-1700-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42957/download/46625/ST-1800-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42958/download/46626/ST-1900-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42959/download/46627/ST-2000-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42960/download/46628/ST-2100-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42961/download/46629/ST-2200-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42962/download/46630/ST-2300-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42963/download/46631/ST-2400-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42964/download/46632/ST-2500-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42965/download/46633/ST-2600-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42966/download/46634/ST-2700-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42967/download/46635/ST-2800-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42968/download/46636/ST-2900-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42969/download/46637/ST-3000-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42970/download/46638/ST-3100-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42971/download/46639/ST-3200-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42972/download/46640/ST-3300-PCA-A-11-ddw.xlsx",
   "https://censusindia.gov.in/nada/index.php/catalog/42973/download/46641/ST-3500-PCA-A-11-ddw.xlsx"
  ]
 }
}
