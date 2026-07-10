-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Performer" AS performer,
    "Score per year" AS score_per_year,
    "Total score" AS total_score,
    "Show" AS show
FROM "fivethirtyeight-mad-men-performer-scores"
