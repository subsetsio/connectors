-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "edition",
    "edition_id",
    "country_noc",
    "sport",
    "event",
    "result_id",
    "athlete",
    "athlete_id",
    "position",
    "medal",
    "is_team_sport"
FROM "base-dos-dados-world-olympedia-olympics--athlete-event-result"
