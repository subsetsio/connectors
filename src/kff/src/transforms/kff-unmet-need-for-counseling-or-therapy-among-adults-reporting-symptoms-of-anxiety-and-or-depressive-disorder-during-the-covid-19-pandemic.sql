-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one cell from a KFF State Health Facts indicator table; do not sum across metrics or locations without first selecting the desired metric/timeframe and excluding aggregate locations when appropriate.
SELECT
    "location",
    "timeframe",
    "col_index",
    "metric",
    "value_raw",
    "value"
FROM "kff-unmet-need-for-counseling-or-therapy-among-adults-reporting-symptoms-of-anxiety-and-or-depressive-disorder-during-the-covid-19-pandemic"
