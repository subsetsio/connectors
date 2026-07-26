-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "subdistrict",
    "november_2017_identified_need",
    "february_2018_funded_need",
    "additional_need_unfunded",
    "number_of_seats_in_scope_design"
FROM "nyc-open-data-ujdf-5byz"
