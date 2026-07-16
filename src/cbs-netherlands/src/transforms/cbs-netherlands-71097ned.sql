-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "Geschillen_1" AS geschillen_1,
    "VerlorenArbeidsdagen_2" AS verlorenarbeidsdagen_2,
    "BetrokkenWerknemers_3" AS betrokkenwerknemers_3,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71097ned"
