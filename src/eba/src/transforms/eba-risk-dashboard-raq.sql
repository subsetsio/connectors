-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The period is an integer half-year survey code, with Spring encoded as YYYY1 and Autumn encoded as YYYY2.
-- caution: Shares are response distributions by question and answer option; do not sum shares across unrelated questions.
SELECT
    "period",
    "period_label",
    "question",
    "answer",
    "share"
FROM "eba-risk-dashboard-raq"
