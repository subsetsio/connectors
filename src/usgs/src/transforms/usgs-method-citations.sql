-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "method_id",
    "citation_name",
    "citation_method_number",
    "method_source",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-method-citations"
