-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistics" AS statistics,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    CAST("RIS" AS BIGINT) AS ris,
    "Role in public life" AS role_in_public_life,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-megpublirei"
