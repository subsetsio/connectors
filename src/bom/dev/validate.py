import io, tarfile, csv as csvmod, datetime, re, ftplib, duckdb, pyarrow as pa
import sys; sys.path.insert(0, "src")
from nodes.bom import DWO_SCHEMA, _NUM_FIELDS, _num, _DATE_RE, _STATION_RE

ftp = ftplib.FTP("ftp.bom.gov.au", timeout=180); ftp.login("anonymous","x@y.com")
buf=io.BytesIO(); ftp.retrbinary("RETR /anon/gen/clim_data/IDCKWCDEA0.tgz", buf.write); ftp.quit()
cols={f.name:[] for f in DWO_SCHEMA}; n=0
with tarfile.open(fileobj=io.BytesIO(buf.getvalue()), mode="r:gz") as tf:
    for m in tf:
        if not m.isfile() or not m.name.endswith(".csv"): continue
        p=m.name.split("/")
        if len(p)<4: continue
        state,slug=p[1],p[2]
        text=tf.extractfile(m).read().decode("latin-1")
        for row in csvmod.reader(text.splitlines()):
            if len(row)<11 or not _DATE_RE.match(row[1].strip()): continue
            dd,mm,yy=row[1].strip().split("/")
            cols["state"].append(state); cols["station_slug"].append(slug)
            cols["station_name"].append(row[0].strip())
            cols["date"].append(datetime.date(int(yy),int(mm),int(dd)))
            for i,name in enumerate(_NUM_FIELDS,start=2): cols[name].append(_num(row[i]))
            n+=1
        if n>20000: break
t=pa.table({f.name:pa.array(cols[f.name],type=f.type) for f in DWO_SCHEMA}, schema=DWO_SCHEMA)
print("parsed rows:", t.num_rows, "stations:", len(set(cols["station_slug"])))
con=duckdb.connect(); con.register("bom-daily-weather-observations", t)
res=con.execute('''SELECT state,station_slug,station_name,CAST(date AS DATE) AS date,
  evapotranspiration_mm,rainfall_mm,pan_evaporation_mm,max_temp_c,min_temp_c,
  max_relative_humidity_pct,min_relative_humidity_pct,wind_speed_ms,solar_radiation_mj_m2
  FROM "bom-daily-weather-observations" WHERE date IS NOT NULL
  QUALIFY row_number() OVER (PARTITION BY station_slug,date ORDER BY station_name)=1''').fetch_arrow_table()
print("transform rows:", res.num_rows)
print(res.slice(0,3).to_pylist())
