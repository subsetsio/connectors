-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source cube has duplicated dimension combinations in the raw profile, so no row key is declared; treat rows as source observation records rather than a uniquely keyed dimensional cube.
SELECT
    "gender",
    CAST("years" AS BIGINT) AS years,
    "district",
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-08-composition-of-members-elected-in-local-self-governance-body-sakrebulo"
