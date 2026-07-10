-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Castle 1" AS castle_1,
    "Castle 2" AS castle_2,
    "Castle 3" AS castle_3,
    "Castle 4" AS castle_4,
    "Castle 5" AS castle_5,
    "Castle 6" AS castle_6,
    "Castle 7" AS castle_7,
    "Castle 8" AS castle_8,
    "Castle 9" AS castle_9,
    "Castle 10" AS castle_10
FROM "fivethirtyeight-riddler-castles-castle-solutions-4"
