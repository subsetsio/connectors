-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes national, subnational, supranational, and synthetic aggregate areas, so summing across countries or regions can double count.
-- caution: Variable codes encode measure, population, and age concepts; join to the variables table on country and variable to attach labels, units, sources, and methodology before interpreting values.
SELECT
    "country",
    "variable",
    "percentile",
    "year",
    "value",
    "age",
    "pop",
    "data_quality"
FROM "world-inequality-database-values"
