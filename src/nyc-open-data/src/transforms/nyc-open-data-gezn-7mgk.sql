-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ceqr",
    "project_name",
    "project_description",
    "borough",
    "lead_agency",
    "url"
FROM "nyc-open-data-gezn-7mgk"
