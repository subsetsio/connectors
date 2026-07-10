-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains index levels and inflation measures; filter `measure` before comparing or aggregating values.
SELECT
    "date",
    "period",
    "measure",
    "category_code",
    "category_title",
    "weight",
    "base_value",
    "value"
FROM "department-of-census-and-statistics-ccpi"
