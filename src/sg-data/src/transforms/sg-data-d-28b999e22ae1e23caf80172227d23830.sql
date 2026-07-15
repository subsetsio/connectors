-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_property",
    "availability",
    "no_of_private_residential_properties"
FROM "sg-data-d-28b999e22ae1e23caf80172227d23830"
