-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "sex",
    "economic_activity_groupings_aggregated_nomenklature_a17_based_on_nace2003",
    "unit",
    "value"
FROM "statistics-bulgaria-1135"
