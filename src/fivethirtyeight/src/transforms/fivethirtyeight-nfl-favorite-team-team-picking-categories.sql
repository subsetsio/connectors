-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TEAM" AS team,
    "BMK" AS bmk,
    "UNI" AS uni,
    "CCH" AS cch,
    "STX" AS stx,
    "SMK" AS smk,
    "AFF" AS aff,
    "SLP" AS slp,
    "NYP" AS nyp,
    "FRL" AS frl,
    "BNG" AS bng,
    "TRD" AS trd,
    "BWG" AS bwg,
    "FUT" AS fut,
    "PLA" AS pla,
    "OWN" AS own,
    "BEH" AS beh
FROM "fivethirtyeight-nfl-favorite-team-team-picking-categories"
