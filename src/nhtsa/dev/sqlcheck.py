import duckdb, pyarrow as pa
import importlib.util
spec=importlib.util.spec_from_file_location("nhtsa","src/nodes/nhtsa.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def flat_tbl(cols):
    # 2 sample rows of strings
    data={c:["x","" ] for c in cols}
    # plug realistic values for cast targets
    over={"RECORD_ID":["1","2"],"YEARTXT":["2020","9999"],"RCDATE":["20200115",""],
          "ODATE":["20200110",""],"POTAFF":["100",""],"CMPLID":["10","11"],
          "ODINO":["999",""],"INJURED":["1","0"],"DEATHS":["0","0"],"FAILDATE":["20200101",""],
          "DATEA":["20200201",""],"LDATE":["20200205",""],"MILES":["1000",""],
          "YEAR":["2019","9999"],"CDATE":["20200301",""]}
    for k,v in over.items():
        if k in data: data[k]=v
    return pa.table(data, schema=pa.schema([(c,pa.string()) for c in cols]))

views={
 "nhtsa-recalls":flat_tbl(m.RECALLS_COLS),
 "nhtsa-complaints":flat_tbl(m.COMPLAINTS_COLS),
 "nhtsa-investigations":flat_tbl(m.INVESTIGATIONS_COLS),
 "nhtsa-safety-ratings":pa.Table.from_pylist([
    {"VehicleId":123,"ModelYear":2020,"Make":"HONDA","Model":"ACCORD",
     "VehicleDescription":"2020 Honda Accord","OverallRating":"5",
     "OverallFrontCrashRating":"5","OverallSideCrashRating":"5","RolloverRating":"4",
     "RolloverPossibility":0.12,"FrontCrashDriversideRating":"5",
     "FrontCrashPassengersideRating":"5","SideCrashDriversideRating":"5",
     "SideCrashPassengersideRating":"5","SidePoleCrashRating":"5",
     "NHTSAElectronicStabilityControl":"Standard","NHTSAForwardCollisionWarning":"Standard",
     "NHTSALaneDepartureWarning":"Optional","RecallsCount":2,"ComplaintsCount":10,
     "InvestigationCount":1}]),
}
con=duckdb.connect()
for vid,t in views.items():
    con.register(vid.replace("-","_")+"_t", t)
    con.execute(f'CREATE VIEW "{vid}" AS SELECT * FROM {vid.replace("-","_")}_t')
for s in m.TRANSFORM_SPECS:
    try:
        r=con.execute(s.sql).fetch_arrow_table()
        print(f"OK   {s.id}: {r.num_rows} rows, {r.num_columns} cols -> {r.column_names[:6]}...")
    except Exception as e:
        print(f"FAIL {s.id}: {type(e).__name__}: {e}")
