-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    CAST("Value" AS BIGINT) AS value,
    "Unit" AS unit,
    "Series_name" AS series_name,
    "Group" AS group,
    "RBNZ_seriesID" AS rbnz_seriesid
FROM "statsnz-na-isal-march-2026-quarter-supplementary-table-1-5a"
