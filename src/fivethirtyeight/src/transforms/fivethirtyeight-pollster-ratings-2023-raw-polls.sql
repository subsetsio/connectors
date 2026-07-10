-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "poll_id",
    "question_id",
    "race_id",
    "year",
    "race",
    "location",
    "type_simple",
    "type_detail",
    "pollster",
    "pollster_rating_id",
    "methodology",
    "partisan",
    "polldate",
    "samplesize",
    "cand1_name",
    "cand1_id",
    "cand1_party",
    "cand1_pct",
    "cand2_name",
    "cand2_id",
    "cand2_party",
    "cand2_pct",
    "cand3_pct",
    "margin_poll",
    "electiondate",
    "cand1_actual",
    "cand2_actual",
    "margin_actual",
    "error",
    "bias",
    "rightcall",
    "advancedplusminus",
    "comment"
FROM "fivethirtyeight-pollster-ratings-2023-raw-polls"
