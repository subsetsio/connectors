-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("FIGURE" AS BIGINT) AS figure,
    "SETTING" AS setting,
    "INDICATOR" AS indicator,
    "GROUP" AS group,
    "SUBGROUP" AS subgroup,
    CAST("TIME" AS BIGINT) AS time,
    "START_TIME" AS start_time,
    strptime("END_TIME", '%m/%d/%Y')::DATE AS end_time,
    CAST("VALUE" AS DOUBLE) AS value,
    "MEASURE" AS measure
FROM "cdc-gypc-kpgn"
