-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "AA" AS aa,
    "Assembly Area" AS assembly_area,
    "BNKRDIS" AS bnkrdis,
    "Number of participants disposed of in bankruptcies cases" AS number_of_participants_disposed_of_in_bankruptcies_cases,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-bnkrdisaa"
