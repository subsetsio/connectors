-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boro_code",
    "app_num",
    "project_nm",
    "filed_stat",
    "status",
    "effect_dt",
    "bp_num",
    "cc_res_num",
    "zr_update",
    "cert_date",
    "chg_type",
    "altmappdf",
    "altmaplink",
    "scanned",
    "track_num",
    "_source" AS source,
    "map_series",
    "map_cabine",
    "map_copies"
FROM "nyc-open-data-anjb-e5db"
