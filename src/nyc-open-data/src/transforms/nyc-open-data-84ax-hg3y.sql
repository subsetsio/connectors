-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_code",
    "agency_name",
    "fiscal_year",
    "personnel_type",
    "agency_group",
    "city_funds",
    "total_funds"
FROM "nyc-open-data-84ax-hg3y"
