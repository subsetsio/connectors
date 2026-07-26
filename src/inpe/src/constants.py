# Base of the INPE Programa Queimadas "dados abertos" Apache autoindex tree
# (the data.inpe.br/queimadas/dados-abertos/ landing page links out to this host).
CSV_BASE = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv"
ANUAL_BASE = f"{CSV_BASE}/anual"
MENSAL_BASE = f"{CSV_BASE}/mensal"

# Annual reference-satellite directories. INPE's "satélite de referência" series
# is the methodologically-consistent fire-count series used for trend comparison
# across years (a single sensor, AQUA_M-T, the afternoon overpass). These files
# carry a reduced schema: id_bdq, foco_id, lat, lon, data_pas, pais, estado,
# municipio, bioma. NOTE: INPE only creates each year's zip months AFTER the
# year closes (2025's appeared Feb-2026), so these directories never cover the
# current year — the monthly directories below carry the open years.
BRASIL_REF_DIR = f"{ANUAL_BASE}/Brasil_sat_ref"
AMS_REF_DIR = f"{ANUAL_BASE}/AMS_sat_ref"

# Annual all-satellite directory. Carries the richer schema with the satellite
# label plus meteorology/FRP columns: latitude, longitude, data_pas, satelite,
# pais, estado, municipio, bioma, numero_dias_sem_chuva, precipitacao,
# risco_fogo, id_area_industrial, frp. Used for the national series so the
# fire-radiative-power and fire-risk means are available; filtered to the
# reference satellite to stay consistent with the reference count series.
BRASIL_ALLSAT_DIR = f"{ANUAL_BASE}/Brasil_todos_sats"

# Monthly all-satellite directories: one plain CSV per calendar month
# (focos_mensal_br_YYYYMM.csv / focos_mensal_YYYYMM.csv), published within the
# month and updated as the month accrues. Schema: id, lat, lon, data_hora_gmt,
# satelite, municipio, estado, pais, municipio_id, estado_id, pais_id,
# numero_dias_sem_chuva, precipitacao, risco_fogo, bioma, frp. These carry ALL
# satellites; filtering to REFERENCE_SATELLITE continues the reference series
# for years the annual archive does not yet cover.
BRASIL_MENSAL_DIR = f"{MENSAL_BASE}/Brasil"
AMS_MENSAL_DIR = f"{MENSAL_BASE}/America_Sul"

# The reference satellite (AQUA afternoon overpass) — INPE's standard comparison
# sensor since 2002-07-03. Filtering the all-satellite files to this value
# reproduces the reference-series counts while keeping the meteorology/FRP
# columns. Verified still current as of 2026-07: INPE's "situação atual" page
# labels its charts "Apenas Satélite de Referência - AQUA Tarde", and AQUA_M-T
# detections are present in every monthly file through 2026-07 at counts in
# line with prior years. INPE's FAQ says that when AQUA is finally
# decommissioned the reference will move to NPP-SUOMI (VIIRS, ~10x more
# detections) with a cautious series-compatibility adjustment — when that
# happens, update this constant only after INPE publishes the adjusted
# methodology (the fetches fail loudly if a monthly file has zero
# reference-satellite rows, so the switchover cannot pass silently).
REFERENCE_SATELLITE = "AQUA_M-T"
