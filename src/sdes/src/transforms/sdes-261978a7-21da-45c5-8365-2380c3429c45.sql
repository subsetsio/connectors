-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TRIMESTRE" AS trimestre,
    "VEB" AS veb,
    "VEB_1A4" AS veb_1a4,
    "VEB_5A9" AS veb_5a9,
    "VEB_10A19" AS veb_10a19,
    "VEB_20A49" AS veb_20a49,
    "VEB_50PLUS" AS veb_50plus,
    "RESA" AS resa,
    "RESA_COLL" AS resa_coll,
    "RESA_IND" AS resa_ind,
    "RESA_NONSOCIAL" AS resa_nonsocial,
    "RESA_SOCIAL" AS resa_social
FROM "sdes-261978a7-21da-45c5-8365-2380c3429c45"
