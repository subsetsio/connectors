-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Incentive Payment Range" AS incentive_payment_range,
    "Number of Hospitals Receiving this Range" AS number_of_hospitals_receiving_this_range
FROM "cms-vtqa-m4zn"
