-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "geotype",
    "st",
    "geo_id",
    "geo_ttl",
    "geo_id_f",
    "naics",
    "naics_ttl",
    "naics_f",
    "comm",
    "comm_ttl",
    "xmode",
    "xmode_ttl",
    "dmode",
    "dmode_ttl",
    "xdestgeo",
    "xdestgeo_ttl",
    CAST("year" AS BIGINT) AS year,
    CAST("ton" AS BIGINT) AS ton,
    "ton_f",
    CAST("ton_s" AS DOUBLE) AS ton_s,
    "ton_s_f",
    CAST("tonpchg" AS DOUBLE) AS tonpchg,
    "tonpchg_f",
    CAST("tonpchg_s" AS DOUBLE) AS tonpchg_s,
    "tonpchg_s_f",
    CAST("val" AS BIGINT) AS val,
    "val_f",
    CAST("val_s" AS DOUBLE) AS val_s,
    "val_s_f",
    CAST("valpchg" AS DOUBLE) AS valpchg,
    "valpchg_f",
    CAST("valpchg_s" AS DOUBLE) AS valpchg_s,
    "valpchg_s_f"
FROM "u-s-department-of-transportation-qq62-cjjy"
