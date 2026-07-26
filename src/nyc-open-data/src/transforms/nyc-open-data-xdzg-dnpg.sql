-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_number",
    "agency_name",
    "project_type",
    "project_use",
    "number_of_assets"
FROM "nyc-open-data-xdzg-dnpg"
