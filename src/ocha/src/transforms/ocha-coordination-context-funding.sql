-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are appeal funding observations; funding and requirements should be compared within the same appeal_code, location, and reference period.
SELECT
    "resource_hdx_id",
    "appeal_code",
    "appeal_name",
    "appeal_type",
    "requirements_usd",
    "funding_usd",
    "funding_pct",
    "location_code",
    "location_name",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-coordination-context-funding"
