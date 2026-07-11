-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    CAST("MEG" AS BIGINT) AS meg,
    "Minority ethnic group" AS minority_ethnic_group,
    CAST("ACCEPT" AS BIGINT) AS accept,
    "Acceptance" AS acceptance,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-accmeprei"
