-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "edition",
    "edition_id",
    "country",
    "country_noc",
    "gold",
    "silver",
    "bronze",
    "total"
FROM "base-dos-dados-world-olympedia-olympics--game-medal-tally"
