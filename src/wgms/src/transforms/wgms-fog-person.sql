-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "name",
    "surname",
    "original_name",
    "synonyms",
    "orcid",
    "url",
    CAST("birth_year" AS BIGINT) AS birth_year,
    CAST("death_year" AS BIGINT) AS death_year,
    "remarks"
FROM "wgms-fog-person"
