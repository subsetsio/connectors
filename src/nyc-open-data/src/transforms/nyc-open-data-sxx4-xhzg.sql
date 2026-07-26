-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dsny_zone",
    "dsny_district",
    "site_type",
    "site_location",
    "partner",
    "paper_bins",
    "mgp_bins"
FROM "nyc-open-data-sxx4-xhzg"
