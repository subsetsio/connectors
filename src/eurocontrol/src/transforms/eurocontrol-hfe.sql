-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Legacy horizontal flight efficiency publication overlaps conceptually with the current horizontal-flight-efficiency table; avoid combining both tables without deduplicating the publication lineage.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH_NUM" AS BIGINT) AS month_num,
    "MONTH_MON" AS month_mon,
    "ENTRY_DATE" AS entry_date,
    "ENTITY_NAME" AS entity_name,
    "ENTITY_TYPE" AS entity_type,
    "TYPE_MODEL" AS type_model,
    CAST("DIST_FLOWN_KM" AS BIGINT) AS dist_flown_km,
    CAST("DIST_DIRECT_KM" AS DOUBLE) AS dist_direct_km,
    CAST("DIST_ACHIEVED_KM" AS DOUBLE) AS dist_achieved_km,
    "OBS_DATE" AS obs_date
FROM "eurocontrol-hfe"
