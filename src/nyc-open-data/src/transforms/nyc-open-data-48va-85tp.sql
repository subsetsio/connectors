-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gispropnum",
    "propertyname",
    "acres",
    "shape",
    "forverwildid"
FROM "nyc-open-data-48va-85tp"
