-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "category",
    "distinct_donors",
    "number_of_donations",
    "total_weight_short_tons",
    "total_declared_value"
FROM "nyc-open-data-vhtt-kpwy"
