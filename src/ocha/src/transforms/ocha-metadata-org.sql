-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Organization names are not guaranteed to be unique; treat this as a lookup listing rather than a keyed organization registry.
SELECT
    "acronym",
    "name",
    "org_type_code",
    "org_type_description"
FROM "ocha-metadata-org"
