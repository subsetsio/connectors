-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "agency",
    "concessionaire",
    "brief_description_of_concession",
    "concession_award_method",
    "approximate_gross_revenues_received_in_fiscal_year",
    "registration_datestatus",
    "concession_borough"
FROM "nyc-open-data-7bjc-nmt5"
