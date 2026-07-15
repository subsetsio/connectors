-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_property",
    "development_status",
    "no_of_units"
FROM "sg-data-d-7a882bd3d44374a7f701fc6a07620bf8"
