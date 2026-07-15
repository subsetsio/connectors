-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "orders_made",
    "no_order",
    "dismissed",
    "withdrawn",
    "abated",
    "total"
FROM "sg-data-d-87627b915a4169dee01eb89a09b7130c"
