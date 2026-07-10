-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Mixes aggregate rows (professions_detaillees is null) with detailed rows within the same table — filter on the null to pick one level before summing.
SELECT
    "secteur",
    "professions",
    "professions_detaillees",
    CAST("annee" AS BIGINT) AS annee,
    "effectifs"
FROM "drees-effectifs-salaries-hospitaliers-series-longues"
