-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "purpose_type",
    "number_of_vessel_calls",
    "gross_tonnage"
FROM "sg-data-d-48cb38d12697d3463c8cadfb22e6c61d"
