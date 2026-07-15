-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "level",
    "type_of_school",
    "qualification",
    "sex",
    "no_of_teacher",
    "no_of_vice_principal",
    "no_of_principal"
FROM "sg-data-d-8aee2fbb0a3be5f3d49d723c80666766"
