-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial year" AS financial_year,
    "SPNDAREA" AS spndarea,
    "Spending area" AS spending_area,
    "EXPCAT" AS expcat,
    "Expenditure category" AS expenditure_category,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-pubexp"
