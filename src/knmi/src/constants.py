# Dataset config for the KNMI connector — data, not logic.
# Keyed by collect entity id (the spec id minus the "knmi-" prefix).
# Each entry: open-data API dataset name + version, the fetch `mode`, and
# (for matrix climate-normals datasets) the data-file `prefix` to select.
#
# Anonymous public open-data key (Authorization header, raw, no "Bearer").
# Expires 2026-07-01; override via env KNMI_API_KEY (registered/bulk key).
ANON_API_KEY = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6ImVlNDFjMWI0MjlkODQ2MThiNWI4ZDViZDAyMTM2YTM3IiwiaCI6Im11cm11cjEyOCJ9"

CONFIG = {
    "aardbevingen-cijfers-1": {
        "name": "aardbevingen_cijfers", "version": "1", "mode": "earthquakes",
    },
    "waarneemstations-csv-1-0": {
        "name": "waarneemstations_csv", "version": "1.0", "mode": "stations_latest",
    },
    "homogenization-daily-temperature-principal-stations-netherlands-1-0": {
        "name": "homogenization_daily_temperature_principal_stations_netherlands",
        "version": "1.0", "mode": "homogenization",
    },
    "ice-thickness-observations-1-0": {
        "name": "ice_thickness_observations", "version": "1.0", "mode": "ice",
    },
    "climate-normals-1991-2020-climate-normals-by-station-1": {
        "name": "climate_normals_1991_2020_climate_normals_by_station",
        "version": "1", "mode": "matrix", "prefix": "Normalen_",
    },
    "climate-normals-1991-2020-day-normals-by-station-1": {
        "name": "climate_normals_1991_2020_day_normals_by_station",
        "version": "1", "mode": "matrix", "prefix": "Dagnormalen_",
    },
    "climate-normals-1991-2020-per-10-days-by-station-1": {
        "name": "climate_normals_1991_2020_per_10_days_by_station",
        "version": "1", "mode": "matrix", "prefix": "Decadenormalen_",
    },
    "climate-normals-1991-2020-precipitation-normals-by-district-1": {
        "name": "climate_normals_1991_2020_precipitation_normals_by_district",
        "version": "1", "mode": "matrix", "prefix": "Decadenormalen_",
    },
}

ENTITY_IDS = list(CONFIG.keys())
