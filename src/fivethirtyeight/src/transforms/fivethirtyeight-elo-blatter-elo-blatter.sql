-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "elo98",
    "elo15",
    "confederation",
    "gdp06",
    "popu06",
    "gdp_source",
    "popu_source"
FROM "fivethirtyeight-elo-blatter-elo-blatter"
