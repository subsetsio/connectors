-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "infrastructure_type",
    "metric",
    "value",
    "structure_type",
    "year_of_operation"
FROM "qatar-planning-and-statistics-authority-national-digital-infrastructure-overview"
