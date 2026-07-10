-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name" AS name,
    "Description" AS description,
    "URL" AS url,
    "Vendor" AS vendor,
    "Alt. Names / Keywords" AS alt_names_keywords,
    "Subjects" AS subjects,
    "New" AS new,
    "Trial" AS trial,
    "Popular" AS popular
FROM "cdc-sks5-7yq7"
