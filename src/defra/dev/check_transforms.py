import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import duckdb
from nodes import defra as m
from subsets_utils import get

def jget(url, params=None):
    r = get(url, params=params, timeout=(10,120)); r.raise_for_status(); return r.json()

# Build small flattened samples mirroring the fetch fns, then run each transform SQL.
def flat_flood_stations():
    its = jget(f"{m.BASE}/flood-monitoring/id/stations.json", {"_limit":50})["items"]
    return [{"station_reference":it.get("stationReference"),"notation":it.get("notation"),
             "label":m._as_text(it.get("label")),"river_name":m._as_text(it.get("riverName")),
             "catchment_name":m._as_text(it.get("catchmentName")),"town":m._as_text(it.get("town")),
             "lat":it.get("lat"),"long":it.get("long"),"easting":it.get("easting"),"northing":it.get("northing"),
             "date_opened":it.get("dateOpened"),"status":m._last_segment(it.get("status")),"rloi_id":m._as_text(it.get("RLOIid"))} for it in its]

def flat_flood_measures():
    its = jget(f"{m.BASE}/flood-monitoring/id/measures.json", {"_limit":50})["items"]
    return [{"notation":it.get("notation"),"label":m._as_text(it.get("label")),"parameter":m._as_text(it.get("parameter")),
             "parameter_name":m._as_text(it.get("parameterName")),"qualifier":m._as_text(it.get("qualifier")),
             "unit":m._last_segment(it.get("unit")),"unit_name":m._as_text(it.get("unitName")),"period":it.get("period"),
             "value_type":m._as_text(it.get("valueType")),"datum_type":m._last_segment(it.get("datumType")),
             "station_reference":it.get("stationReference")} for it in its]

def flat_flood_readings():
    its = jget(f"{m.BASE}/flood-monitoring/data/readings.json?latest")["items"][:50]
    return [{"measure_id":m._last_segment(it.get("measure")),"measure_uri":it.get("measure") if isinstance(it.get("measure"),str) else None,
             "date_time":it.get("dateTime"),"value":it.get("value")} for it in its]

def flat_flood_areas():
    its = jget(f"{m.BASE}/flood-monitoring/id/floodAreas.json", {"_limit":50})["items"]
    return [{"notation":it.get("notation"),"label":m._as_text(it.get("label")),"description":m._as_text(it.get("description")),
             "county":m._as_text(it.get("county")),"ea_area_name":m._as_text(it.get("eaAreaName")),
             "river_or_sea":m._as_text(it.get("riverOrSea")),"fwd_code":m._as_text(it.get("fwdCode")),
             "quick_dial_number":m._as_text(it.get("quickDialNumber")),"lat":it.get("lat"),"long":it.get("long")} for it in its]

def flat_hydro_stations():
    its = jget(f"{m.BASE}/hydrology/id/stations.json", {"_limit":50})["items"]
    return [{"notation":it.get("notation"),"label":m._as_text(it.get("label")),"river_name":m._as_text(it.get("riverName")),
             "lat":it.get("lat"),"long":it.get("long"),"easting":it.get("easting"),"northing":it.get("northing"),
             "date_opened":it.get("dateOpened"),"status":m._last_segment(it.get("status")),
             "station_guid":m._as_text(it.get("stationGuid")),"wiski_id":m._as_text(it.get("wiskiID"))} for it in its]

def flat_hydro_measures():
    its = jget(f"{m.BASE}/hydrology/id/measures.json", {"_limit":50})["items"]
    return [{"notation":it.get("notation"),"label":m._as_text(it.get("label")),"parameter":m._as_text(it.get("parameter")),
             "parameter_name":m._as_text(it.get("parameterName")),"observed_property":m._last_segment(it.get("observedProperty")),
             "period":it.get("period"),"period_name":m._as_text(it.get("periodName")),"value_statistic":m._last_segment(it.get("valueStatistic")),
             "unit":m._last_segment(it.get("unit")),"unit_name":m._as_text(it.get("unitName")),"station":m._last_segment(it.get("station")),
             "observation_type":m._last_segment(it.get("observationType"))} for it in its]

def flat_hydro_readings():
    its = jget(f"{m.BASE}/hydrology/data/readings.json", {"date":"2026-06-20","_limit":50})["items"]
    return [{"measure_id":m._last_segment(it.get("measure")),"date":it.get("date"),"date_time":it.get("dateTime"),
             "value":it.get("value"),"quality":m._as_text(it.get("quality"))} for it in its]

samplers = {
 "defra-flood-monitoring-stations": flat_flood_stations,
 "defra-flood-monitoring-measures": flat_flood_measures,
 "defra-flood-monitoring-readings": flat_flood_readings,
 "defra-flood-monitoring-floods": flat_flood_areas,
 "defra-hydrology-stations": flat_hydro_stations,
 "defra-hydrology-measures": flat_hydro_measures,
 "defra-hydrology-readings": flat_hydro_readings,
}

con = duckdb.connect()
for spec in m.TRANSFORM_SPECS:
    dep = spec.deps[0]
    rows = samplers[dep]()
    tf = tempfile.NamedTemporaryFile("w", suffix=".ndjson", delete=False)
    for r in rows: tf.write(json.dumps(r)+"\n")
    tf.close()
    con.execute(f'''CREATE OR REPLACE VIEW "{dep}" AS SELECT * FROM read_json_auto('{tf.name}', format='newline_delimited')''')
    try:
        res = con.execute(spec.sql).fetchall()
        cols = [d[0] for d in con.execute(spec.sql).description]
        print(f"OK  {spec.id}: {len(res)} rows, cols={cols}")
    except Exception as e:
        print(f"ERR {spec.id}: {type(e).__name__}: {e}")
