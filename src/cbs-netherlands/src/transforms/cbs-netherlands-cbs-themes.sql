-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ID" AS id,
    "ParentID" AS parentid,
    "Number" AS number,
    "Title" AS title,
    "Language" AS language,
    "Catalog" AS catalog
FROM "cbs-netherlands-cbs-themes"
