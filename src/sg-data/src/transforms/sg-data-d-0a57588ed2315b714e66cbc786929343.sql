-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "gross_monthly_income_excl_emr_cpf",
    "employment_status",
    "employed"
FROM "sg-data-d-0a57588ed2315b714e66cbc786929343"
