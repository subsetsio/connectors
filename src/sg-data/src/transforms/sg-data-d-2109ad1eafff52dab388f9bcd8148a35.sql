-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "type_of_property",
    "annual_value",
    "tax_rate"
FROM "sg-data-d-2109ad1eafff52dab388f9bcd8148a35"
