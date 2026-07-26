-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_birth",
    "gender",
    "ethnicity",
    "childs_first_name",
    "count",
    "rank"
FROM "nyc-open-data-25th-nujf"
