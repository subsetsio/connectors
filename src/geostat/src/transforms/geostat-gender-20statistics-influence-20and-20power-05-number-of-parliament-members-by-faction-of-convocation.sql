-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "factions_of_convocation",
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-05-number-of-parliament-members-by-faction-of-convocation"
