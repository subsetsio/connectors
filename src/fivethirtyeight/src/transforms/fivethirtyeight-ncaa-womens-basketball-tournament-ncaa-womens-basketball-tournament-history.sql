-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "School" AS school,
    "Seed" AS seed,
    "Conference" AS conference,
    "Conf. W" AS conf_w,
    "Conf. L" AS conf_l,
    "Conf. %" AS conf,
    "Conf. place" AS conf_place,
    "Reg. W" AS reg_w,
    "Reg. L" AS reg_l,
    "Reg. %" AS reg,
    "How qual" AS how_qual,
    "1st game at home?" AS "1st_game_at_home",
    "Tourney W" AS tourney_w,
    "Tourney L" AS tourney_l,
    "Tourney finish" AS tourney_finish,
    "Full W" AS full_w,
    "Full L" AS full_l,
    "Full %" AS full
FROM "fivethirtyeight-ncaa-womens-basketball-tournament-ncaa-womens-basketball-tournament-history"
