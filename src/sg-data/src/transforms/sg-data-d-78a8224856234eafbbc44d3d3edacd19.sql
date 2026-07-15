-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "course",
    "intake",
    "enrolment",
    "graduates"
FROM "sg-data-d-78a8224856234eafbbc44d3d3edacd19"
