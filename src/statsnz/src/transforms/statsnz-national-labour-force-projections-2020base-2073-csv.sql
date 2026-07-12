-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "Characteristic" AS characteristic,
    "P05" AS p05,
    "P25" AS p25,
    "P50" AS p50,
    "P75" AS p75,
    "P95" AS p95,
    CAST("sortorder" AS BIGINT) AS sortorder
FROM "statsnz-national-labour-force-projections-2020base-2073-csv"
