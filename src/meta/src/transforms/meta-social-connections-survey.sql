-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are aggregated survey responses; filter by variable or question_text before comparing the value column across countries.
SELECT
    "country",
    "variable",
    "value",
    "estimate_weighted",
    "estimate_weighted_se",
    "estimate_weighted_95ci_low",
    "estimate_weighted_95ci_upp",
    "n_unweighted",
    "question_text",
    "notes",
    "_source_file" AS source_file
FROM "meta-social-connections-survey"
