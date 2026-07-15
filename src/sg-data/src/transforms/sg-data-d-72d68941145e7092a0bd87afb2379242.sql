-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "place_of_occurrence",
    "infant_indicator",
    "death_count"
FROM "sg-data-d-72d68941145e7092a0bd87afb2379242"
