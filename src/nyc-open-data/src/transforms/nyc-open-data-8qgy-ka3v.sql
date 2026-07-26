-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "recreation_unit",
    "acres",
    "county",
    "town",
    "wmu",
    "status",
    "_map" AS map,
    "_label" AS label,
    "lastmodifi"
FROM "nyc-open-data-8qgy-ka3v"
