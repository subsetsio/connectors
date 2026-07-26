-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "percent_project",
    "artist",
    "address",
    "zip_code",
    "borough",
    "design_agency",
    "sponsor_agency"
FROM "nyc-open-data-gzdv-qiga"
