-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "employees_bound_to_a_covenant_not_to_compete_confidentiality_commitment",
    "group_of_enterprises",
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-tku65.px"
