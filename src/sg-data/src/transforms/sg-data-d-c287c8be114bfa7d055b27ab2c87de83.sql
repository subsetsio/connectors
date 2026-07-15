-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_sale",
    "sale_status",
    "units"
FROM "sg-data-d-c287c8be114bfa7d055b27ab2c87de83"
