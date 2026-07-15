-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "profession",
    "no_per_1000",
    "ratio_to_population"
FROM "sg-data-d-391082b04c131ce998277673fbd2fe13"
