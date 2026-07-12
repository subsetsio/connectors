-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "satisfaction_with_a_possibility_to_have_a_say_in_enterprise_s_activity",
    "group_of_employees",
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-tku21.px"
