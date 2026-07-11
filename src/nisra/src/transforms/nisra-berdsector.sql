-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistics" AS statistics,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Financial year" AS BIGINT) AS financial_year,
    "BERDSECTOR" AS berdsector,
    "Industry Subsection" AS industry_subsection,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-berdsector"
