# Base of the INPE Programa Queimadas "dados abertos" Apache autoindex tree
# (the data.inpe.br/queimadas/dados-abertos/ landing page links out to this host).
DATASERVER_BASE = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual"

# Annual reference-satellite directories. INPE's "satélite de referência" series
# is the methodologically-consistent fire-count series used for trend comparison
# across years (a single sensor, AQUA_M-T, the afternoon overpass). These files
# carry a reduced schema: id_bdq, foco_id, lat, lon, data_pas, pais, estado,
# municipio, bioma.
BRASIL_REF_DIR = f"{DATASERVER_BASE}/Brasil_sat_ref"
AMS_REF_DIR = f"{DATASERVER_BASE}/AMS_sat_ref"

# Annual all-satellite directory. Carries the richer schema with the satellite
# label plus meteorology/FRP columns: latitude, longitude, data_pas, satelite,
# pais, estado, municipio, bioma, numero_dias_sem_chuva, precipitacao,
# risco_fogo, id_area_industrial, frp. Used for the national series so the
# fire-radiative-power and fire-risk means are available; filtered to the
# reference satellite to stay consistent with the reference count series.
BRASIL_ALLSAT_DIR = f"{DATASERVER_BASE}/Brasil_todos_sats"

# The reference satellite (AQUA afternoon overpass) — INPE's standard comparison
# sensor. Filtering the all-satellite files to this value reproduces the
# reference-series counts while keeping the meteorology/FRP columns.
REFERENCE_SATELLITE = "AQUA_M-T"
