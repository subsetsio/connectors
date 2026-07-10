-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "scenes",
    "bill_nighy",
    "keira_knightley",
    "andrew_lincoln",
    "hugh_grant",
    "colin_firth",
    "alan_rickman",
    "heike_makatsch",
    "laura_linney",
    "emma_thompson",
    "liam_neeson",
    "kris_marshall",
    "abdul_salis",
    "martin_freeman",
    "rowan_atkinson"
FROM "fivethirtyeight-love-actually-love-actually-appearances"
