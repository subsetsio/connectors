-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "male",
    "female",
    "total"
FROM "sg-data-d-45e3404079cd3f67543f4f29e468a54e"
