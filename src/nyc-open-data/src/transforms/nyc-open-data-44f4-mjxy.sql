-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "client_id",
    "request_date",
    "request_id",
    "request_category",
    "request_subcategory",
    "client_affiliation",
    "vetmil_status",
    "character_of_discharge",
    "gender_identification",
    "race",
    "hispaniclatino",
    "marital_status",
    "zip_code",
    "report_fiscal_year"
FROM "nyc-open-data-44f4-mjxy"
