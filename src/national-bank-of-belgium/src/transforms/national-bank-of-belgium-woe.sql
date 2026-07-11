-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one NBB.Stat SDMX dataflow; dimensions and attributes are source-specific codes, so filter the relevant dimensions before aggregating observations.
SELECT
    "DATAFLOW" AS dataflow,
    "DATA_DOMAIN" AS data_domain,
    "REF_AREA" AS ref_area,
    "INDICATOR" AS indicator,
    "COUNTERPART_AREA" AS counterpart_area,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    "COMMENT" AS comment,
    CAST("BASE_PER" AS BIGINT) AS base_per,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "OBS_STATUS" AS obs_status,
    "TIME_FORMAT" AS time_format
FROM "national-bank-of-belgium-woe"
