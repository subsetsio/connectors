-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "possibility_to_determine_one_s_work_pace",
    "group_of_employees",
    "indicator",
    CAST("yera" AS BIGINT) AS yera,
    "value"
FROM "statistics-estonia-tku70.px"
