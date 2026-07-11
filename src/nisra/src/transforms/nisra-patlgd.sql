-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial year" AS financial_year,
    "LGD2014" AS lgd2014,
    "Local Government District" AS local_government_district,
    CAST("PAS" AS BIGINT) AS pas,
    "Application status" AS application_status,
    "PAT" AS pat,
    "Application type" AS application_type,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-patlgd"
