-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "month",
    CAST("SA2_code" AS BIGINT) AS sa2_code,
    "SA2_name" AS sa2_name,
    "territorial_authority",
    CAST("total_dwelling_units" AS BIGINT) AS total_dwelling_units,
    CAST("houses" AS BIGINT) AS houses,
    CAST("apartments" AS BIGINT) AS apartments,
    CAST("retirement_village_units" AS BIGINT) AS retirement_village_units,
    CAST("townhouses_flats_units_other" AS BIGINT) AS townhouses_flats_units_other
FROM "statsnz-new-dwellings-consented-by-statistical-area-2-may-2026"
