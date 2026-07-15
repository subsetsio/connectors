-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sn",
    "cluster",
    "satellite_office",
    "address",
    "postal_code",
    "telephone_1",
    "telephone_2"
FROM "sg-data-d-585344026a85579273007a1eb048d4da"
