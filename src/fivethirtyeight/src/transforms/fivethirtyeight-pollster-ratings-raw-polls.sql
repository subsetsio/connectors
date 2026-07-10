-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "poll_id",
    "question_id",
    "race_id",
    "cycle",
    "location",
    "type_simple",
    "race",
    "pollster",
    "pollster_rating_id",
    "aapor_roper",
    "inactive",
    "methodology",
    "transparency_score",
    "partisan",
    "polldate",
    "electiondate",
    "time_to_election",
    "samplesize",
    "cand1_name",
    "cand1_id",
    "cand1_party",
    "cand1_pct",
    "cand1_actual",
    "cand2_name",
    "cand2_id",
    "cand2_party",
    "cand2_pct",
    "cand2_actual",
    "margin_poll",
    "margin_actual"
FROM "fivethirtyeight-pollster-ratings-raw-polls"
