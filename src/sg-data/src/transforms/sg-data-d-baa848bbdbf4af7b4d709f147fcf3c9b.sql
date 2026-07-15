-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_property",
    "development_status",
    "no_of_units"
FROM "sg-data-d-baa848bbdbf4af7b4d709f147fcf3c9b"
