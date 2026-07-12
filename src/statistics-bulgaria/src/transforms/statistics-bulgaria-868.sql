-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("period" AS BIGINT) AS period,
    "aggregated_nomenclature_of_economic_activities_a21_2008",
    "size_class_by_employed",
    "indicators",
    "unit",
    "value"
FROM "statistics-bulgaria-868"
