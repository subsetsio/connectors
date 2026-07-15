-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "immunisation_type",
    "sector",
    "number_of_children"
FROM "sg-data-d-1ddbedb29e8d6da52c77b10ad92a7134"
