-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OBEC" AS BIGINT) AS obec,
    CAST("OKRSEK" AS BIGINT) AS okrsek,
    CAST("KC1" AS BIGINT) AS kc1,
    "NAZEVOKRSK" AS nazevokrsk,
    "TYPURADU" AS typuradu,
    CAST("KODZEME" AS BIGINT) AS kodzeme,
    "ZKRZEME" AS zkrzeme,
    "NAZEVZEME" AS nazevzeme,
    "SVETADIL" AS svetadil,
    CAST("CASPOSUNLC" AS BIGINT) AS casposunlc,
    "NAZEVOKRSA" AS nazevokrsa,
    "NAZEVZEMEA" AS nazevzemea,
    "SUBKONTINENT" AS subkontinent
FROM "czech-statistical-office-ps2021psrzvo"
