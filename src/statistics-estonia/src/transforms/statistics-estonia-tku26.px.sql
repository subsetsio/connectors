-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "satisfaction_with_possibilities_to_gain_new_skills_and_knowledge_at_work",
    "group_of_employees",
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-tku26.px"
