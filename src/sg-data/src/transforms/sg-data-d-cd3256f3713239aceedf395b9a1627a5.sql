-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "zakat_nisab_rates",
    "Corrected" AS corrected
FROM "sg-data-d-cd3256f3713239aceedf395b9a1627a5"
