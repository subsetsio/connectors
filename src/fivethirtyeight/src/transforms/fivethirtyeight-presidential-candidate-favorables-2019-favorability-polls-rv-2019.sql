-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "question_id",
    "start_date",
    "end_date",
    "pollster_id",
    "pollster",
    "sponsors",
    "sample_size",
    "population",
    "methodology",
    "url",
    "politician",
    "favorable",
    "unfavorable",
    "very_favorable",
    "somewhat_favorable",
    "somewhat_unfavorable",
    "very_unfavorable"
FROM "fivethirtyeight-presidential-candidate-favorables-2019-favorability-polls-rv-2019"
