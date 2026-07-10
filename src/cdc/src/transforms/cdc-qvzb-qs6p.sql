-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Age Group (years)" AS age_group_years,
    "Site" AS site,
    CAST("Year" AS BIGINT) AS year,
    "IPD Serotype" AS ipd_serotype,
    CAST("Frequency Count" AS BIGINT) AS frequency_count
FROM "cdc-qvzb-qs6p"
