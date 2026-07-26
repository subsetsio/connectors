-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency",
    "median_cycle_time_agency",
    "citywide_median_cycle_time"
FROM "nyc-open-data-tdhn-vze8"
