-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "movie",
    "bechdel",
    "peirce",
    "landau",
    "feldman",
    "villareal",
    "hagen",
    "ko",
    "villarobos",
    "waithe",
    "koeze_dottle",
    "uphold",
    "white",
    "rees-davies" AS rees_davies
FROM "fivethirtyeight-next-bechdel-nextbechdel-alltests"
