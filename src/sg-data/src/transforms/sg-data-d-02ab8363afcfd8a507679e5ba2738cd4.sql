-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "tariff_cent_per_kwh"
FROM "sg-data-d-02ab8363afcfd8a507679e5ba2738cd4"
