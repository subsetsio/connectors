-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial year" AS financial_year,
    "WMDW" AS wmdw,
    "Washing machine/dishwasher" AS washing_machine_dishwasher,
    CAST("WMDW_USE" AS BIGINT) AS wmdw_use,
    "Average use" AS average_use,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-water06a07a"
