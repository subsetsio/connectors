-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "election_subject",
    "parties",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-14-number-of-candidates-nominated-by-political-parties-in-parliamentary-elections-of-georgia-in-2016"
