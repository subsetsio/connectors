-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "doe_students",
    "doe_sth",
    "doe_sth_1",
    "charter_students",
    "charter_sth",
    "charter_sth_1"
FROM "nyc-open-data-vgqq-m7ux"
