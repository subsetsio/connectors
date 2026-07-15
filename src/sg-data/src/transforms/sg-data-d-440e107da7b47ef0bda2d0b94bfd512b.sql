-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_workers_covered",
    "no._certified" AS no_certified
FROM "sg-data-d-440e107da7b47ef0bda2d0b94bfd512b"
