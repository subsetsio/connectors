-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Language ranks are within each reporting entity and year, not globally comparable ranks.
SELECT
    "report_year",
    "entity_name",
    "home_language",
    "entity_cd",
    "language_rank",
    "school_year",
    CAST("institution_id" AS BIGINT) AS institution_id
FROM "new-york-state-education-department-ell-home-languages"
