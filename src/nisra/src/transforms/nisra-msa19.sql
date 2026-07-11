-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census Year" AS BIGINT) AS census_year,
    "COB_HIST" AS cob_hist,
    "Country of Birth" AS country_of_birth,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-msa19"
