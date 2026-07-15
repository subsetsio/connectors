-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sick_leave",
    "proportion"
FROM "sg-data-d-f66ad192831ee7295a97f5117a08fdb7"
