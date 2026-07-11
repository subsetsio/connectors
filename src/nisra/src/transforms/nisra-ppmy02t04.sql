-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "Sex" AS sex,
    "Sex Label" AS sex_label,
    CAST("fiveyrage" AS BIGINT) AS fiveyrage,
    "Five year age bands" AS five_year_age_bands,
    "Variant" AS variant,
    "Variant Label" AS variant_label,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-ppmy02t04"
