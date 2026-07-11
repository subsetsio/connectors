-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "ELB" AS elb,
    "Education and Library Board" AS education_and_library_board,
    CAST("5yrage" AS BIGINT) AS five_year_age_code,
    "Five year age bands" AS five_year_age_bands,
    "Sex" AS sex,
    "Sex Label" AS sex_label,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-ppmy01t04"
