-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "profile_id",
    "date",
    "case_number",
    "charge_description",
    "disposition",
    "penalty_and_quantity",
    "export_date"
FROM "nyc-open-data-uafj-ik29"
