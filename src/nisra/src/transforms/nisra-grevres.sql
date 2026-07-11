-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Year" AS year,
    CAST("GENDER" AS BIGINT) AS gender,
    "Gender Label" AS gender_label,
    "GRAGERANGE" AS gragerange,
    "Age ranges for good relations projects" AS age_ranges_for_good_relations_projects,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-grevres"
