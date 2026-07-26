-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "department",
    "services",
    "estimated_cost_of_service_per_contract",
    "anticipated_number_of_contracts",
    "data_as_of_date"
FROM "nyc-open-data-p8e4-uwuv"
