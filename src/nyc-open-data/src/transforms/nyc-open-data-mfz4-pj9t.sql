-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency",
    "rfps_released_in_fiscal_year",
    "citywide_median_calendar_days_rfp_release_to_award"
FROM "nyc-open-data-mfz4-pj9t"
