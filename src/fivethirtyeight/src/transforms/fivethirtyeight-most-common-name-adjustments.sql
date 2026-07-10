-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "Miller" AS miller,
    "Anderson" AS anderson,
    "Martin" AS martin,
    "Smith" AS smith,
    "Thompson" AS thompson,
    "Wilson" AS wilson,
    "Moore" AS moore,
    "White" AS white,
    "Taylor" AS taylor,
    "Davis" AS davis,
    "Johnson" AS johnson,
    "Brown" AS brown,
    "Jones" AS jones,
    "Thomas" AS thomas,
    "Williams" AS williams,
    "Jackson" AS jackson,
    "Lee" AS lee,
    "Garcia" AS garcia,
    "Martinez" AS martinez,
    "Rodriguez" AS rodriguez
FROM "fivethirtyeight-most-common-name-adjustments"
