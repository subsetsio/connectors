-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "voorkeelte_oskus",
    "sugu",
    CAST("aasta" AS BIGINT) AS aasta,
    "vanuseruhm",
    "elukoht",
    "value"
FROM "statistics-estonia-rlv439.px"
