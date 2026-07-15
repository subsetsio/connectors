-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "sex",
    "total_net_enrolment_rate"
FROM "sg-data-d-687d662410ec92ccc11835f057cfc9f7"
