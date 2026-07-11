-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "INDIC_DE" AS indic_de,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-d96c6d1d-ee4b-483d-bfab-4b0baaae5e55"
