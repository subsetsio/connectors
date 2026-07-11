-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial year" AS financial_year,
    CAST("HIGHEST_QUALIFICATION_AGG3" AS BIGINT) AS highest_qualification_agg3,
    "Highest level of qualification" AS highest_level_of_qualification,
    CAST("INTFUN" AS BIGINT) AS intfun,
    "Internet function" AS internet_function,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-bdsifqual"
