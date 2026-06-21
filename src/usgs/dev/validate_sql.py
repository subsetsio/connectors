import json, gzip, os, tempfile, sys
import duckdb
sys.path.insert(0, "src")
from nodes.usgs import TRANSFORM_SPECS

S = {
 "monitoring-locations": {"id":"USGS-01","monitoring_location_number":"01646500","monitoring_location_name":"Potomac","agency_code":"USGS","agency_name":"US Geological Survey","site_type":"Stream","site_type_code":"ST","state_name":"Virginia","county_name":"Fairfax","country_name":"US","hydrologic_unit_code":"02070008","aquifer_code":"100","national_aquifer_code":"N100","altitude":"37.5","drainage_area":"11560","construction_date":"1930-01-01","revision_modified":"2024-01-01T00:00:00Z","_lon":"-77.1","_lat":"38.9"},
 "peaks": {"id":"P1","monitoring_location_id":"USGS-01","parameter_code":"00060","water_year":"2020","value":"123.4","unit_of_measure":"ft3/s","qualifier":"","time":"2020-03-15","peak_since":"","last_modified":"2024-01-01T00:00:00Z","_lon":None,"_lat":None},
 "daily": {"monitoring_location_id":"USGS-01","parameter_code":"00060","statistic_id":"00003","time_series_id":"TS1","time":"2024-06-01","value":"55.5","unit_of_measure":"ft3/s","qualifier":"A","approval_status":"Approved","last_modified":"2024-06-02T00:00:00Z","_lon":None,"_lat":None},
 "continuous": {"monitoring_location_id":"USGS-01","parameter_code":"00065","statistic_id":"","time_series_id":"TS2","time":"2024-06-01T12:00:00Z","value":"3.21","unit_of_measure":"ft","qualifier":"A","approval_status":"Approved","last_modified":"2024-06-02T00:00:00Z","_lon":None,"_lat":None},
 "field-measurements": {"field_measurements_series_id":"FM1","field_visit_id":"FV1","monitoring_location_id":"USGS-01","parameter_code":"00060","value":"60.1","unit_of_measure":"ft3/s","time":"2024-05-01T10:00:00Z","reading_type":"Routine","measuring_agency":"USGS","qualifier":"","last_modified":"2024-05-02T00:00:00Z","_lon":None,"_lat":None},
 "channel-measurements": {"id":"C1","field_visit_id":"FV1","monitoring_location_id":"USGS-01","measurement_number":"5","measurement_type":"ADCP","channel_material":"Sand","channel_name":"main","channel_width":"40.2","channel_width_unit":"ft","channel_area":"120.0","channel_area_unit":"ft2","channel_velocity":"1.5","channel_velocity_unit":"ft/s","channel_flow":"180.0","channel_flow_unit":"ft3/s","time":"2024-05-01T10:00:00Z","last_modified":"2024-05-02T00:00:00Z","_lon":None,"_lat":None},
 "combined-metadata": {"id":"CM1","monitoring_location_id":"USGS-01","monitoring_location_name":"Potomac","agency_code":"USGS","site_type":"Stream","state_name":"Virginia","county_name":"Fairfax","parameter_code":"00060","parameter_name":"Discharge","statistic_id":"00003","computation_identifier":"X","data_type":"daily","unit_of_measure":"ft3/s","begin":"2000-01-01T00:00:00Z","end":"2024-01-01T00:00:00Z","last_modified":"2024-01-02T00:00:00Z","_lon":"-77.1","_lat":"38.9"},
 "time-series-metadata": {"id":"TSM1","monitoring_location_id":"USGS-01","parameter_code":"00060","parameter_name":"Discharge","statistic_id":"00003","computation_identifier":"X","computation_period_identifier":"Daily","unit_of_measure":"ft3/s","begin":"2000-01-01T00:00:00Z","end":"2024-01-01T00:00:00Z","begin_utc":"2000-01-01T05:00:00Z","end_utc":"2024-01-01T05:00:00Z","state_name":"Virginia","hydrologic_unit_code":"02070008","web_description":"desc","last_modified":"2024-01-02T00:00:00Z","_lon":None,"_lat":None},
}
EQ = {"time":"2024-01-01T23:55:54.690Z","latitude":"33.4","longitude":"-116.6","depth":"6.1","mag":"0.65","magType":"ml","nst":"32","gap":"76","dmin":"0.08","rms":"0.15","net":"ci","id":"ci40453703","updated":"2024-01-03T19:25:30.545Z","place":"15 km S of Anza, CA","type":"earthquake","horizontalError":"0.21","depthError":"0.6","magError":"0.16","magNst":"8","status":"reviewed","locationSource":"ci","magSource":"ci"}

tmpd = tempfile.mkdtemp()
def write(asset, rows):
    p = os.path.join(tmpd, asset + ".ndjson.gz")
    with gzip.open(p, "wt") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return p

con = duckdb.connect()
ok = True
for spec in TRANSFORM_SPECS:
    dep = spec.deps[0]
    coll = dep[len("usgs-"):]
    if coll == "earthquakes":
        r1 = dict(EQ); r2 = dict(EQ); r2["id"] = "ci999"; r2["time"] = "2024-01-02T00:00:00.000Z"
    else:
        base = S[coll]; r1 = dict(base); r2 = dict(base)
        for kf in ("id", "time", "time_series_id", "field_measurements_series_id", "monitoring_location_id"):
            if kf in r2 and r2[kf]:
                r2[kf] = str(r2[kf]) + "-2"; break
    path = write(dep, [r1, r2, dict(r1)])  # dup of r1 tests DISTINCT
    con.execute('CREATE OR REPLACE TEMP VIEW "' + dep + '" AS SELECT * FROM read_json_auto(\'' + path + '\')')
    try:
        rel = con.execute(spec.sql)
        cols = [d[0] for d in rel.description]
        res = rel.fetchall()
        flag = "  !!! ZERO ROWS" if len(res) == 0 else ""
        print("OK   %-42s rows=%d cols=%d%s" % (spec.id, len(res), len(cols), flag))
        if len(res) == 0:
            ok = False
    except Exception as e:
        ok = False
        print("FAIL %-42s %s: %s" % (spec.id, type(e).__name__, e))
print("ALL OK" if ok else "HAD FAILURES")
