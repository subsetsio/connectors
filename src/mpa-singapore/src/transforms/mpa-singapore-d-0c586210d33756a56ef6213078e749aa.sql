-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "number_of_vessels",
    "gross_tonnage"
FROM "mpa-singapore-d-0c586210d33756a56ef6213078e749aa"
