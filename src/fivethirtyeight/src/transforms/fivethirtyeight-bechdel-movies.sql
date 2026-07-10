-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "imdb",
    "title",
    "test",
    "clean_test",
    "binary",
    "budget",
    "domgross",
    "intgross",
    "code",
    "budget_2013$" AS budget_2013,
    "domgross_2013$" AS domgross_2013,
    "intgross_2013$" AS intgross_2013,
    "period code" AS period_code,
    "decade code" AS decade_code
FROM "fivethirtyeight-bechdel-movies"
