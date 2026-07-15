-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course",
    "enrolment"
FROM "sg-data-d-67e5b17dfd7a81c68df40dc5afb2a759"
