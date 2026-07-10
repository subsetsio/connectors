-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "year",
    CAST("period" AS BIGINT) AS period,
    "indicator_code",
    "indicator_title",
    "units",
    "value"
FROM "department-of-census-and-statistics-glance-tnteach"
