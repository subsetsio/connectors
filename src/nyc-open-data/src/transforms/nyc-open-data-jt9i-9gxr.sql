-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "description",
    "epp_minimum_standard_indicated",
    "contract_start_end_dates",
    "registration_date",
    "contract_value"
FROM "nyc-open-data-jt9i-9gxr"
