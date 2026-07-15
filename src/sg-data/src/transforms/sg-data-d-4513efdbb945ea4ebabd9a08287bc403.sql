-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_workers_covered",
    "no._awarded" AS no_awarded
FROM "sg-data-d-4513efdbb945ea4ebabd9a08287bc403"
