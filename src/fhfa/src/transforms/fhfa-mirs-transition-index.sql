-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "release_date",
    CAST("index_value" AS DOUBLE) AS index_value
FROM "fhfa-mirs-transition-index"
