-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "caseload_type",
    "hpu_unit",
    "gramercy_center",
    "garrison_center",
    "crotona",
    "hamilton",
    "amsterdam",
    "kingsbridge",
    "jerome",
    "queensboro",
    "coney_island",
    "brownsville",
    "greenwood",
    "richmond_staten_island",
    "grand_concourse",
    "service",
    "total"
FROM "nyc-open-data-uwx4-aafe"
