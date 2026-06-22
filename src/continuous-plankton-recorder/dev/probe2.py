import io, os, tempfile, zipfile, duckdb
# reuse the already-downloaded /tmp zip to avoid re-download
blob = open('/tmp/bco-dmo.zip','rb').read()
with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        zf.extract("occurrence.txt", tmp)
    occ = os.path.join(tmp,"occurrence.txt")
    con=duckdb.connect()
    rel=con.sql("SELECT * FROM read_csv('%s', delim='\\t', header=true, all_varchar=true, quote='', nullstr='')" % occ)
    con.execute("CREATE TABLE raw AS SELECT * FROM read_csv('%s', delim='\\t', header=true, all_varchar=true, quote='', nullstr='')" % occ)
    sql = """
    SELECT occurrenceID AS occurrence_id, eventID AS event_id, catalogNumber AS catalog_number,
      basisOfRecord AS basis_of_record, TRY_CAST(individualCount AS BIGINT) AS individual_count,
      taxonID AS taxon_id, scientificNameID AS scientific_name_id, scientificName AS scientific_name
    FROM raw WHERE occurrenceID IS NOT NULL
    """
    out=con.sql(sql)
    print("transform cols:", out.columns)
    print("rows:", con.sql("SELECT count(*) FROM ("+sql+")").fetchone()[0])
    print(con.sql("SELECT individual_count, scientific_name FROM ("+sql+") LIMIT 3").fetchall())
