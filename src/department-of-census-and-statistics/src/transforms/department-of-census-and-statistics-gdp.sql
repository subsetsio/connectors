-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains annual and quarterly series, current and constant price bases, and value/share/growth measures; filter `frequency`, `price_basis`, and `measure` before comparing or aggregating values.
SELECT
    "date",
    "period",
    "frequency",
    "price_basis",
    "measure",
    "sector_code",
    "sector_title",
    "sector_group",
    "value"
FROM "department-of-census-and-statistics-gdp"
