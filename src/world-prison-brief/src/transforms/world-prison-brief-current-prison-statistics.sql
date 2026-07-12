-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is one named current indicator, and value_text may include units, dates, estimates, or textual qualifiers rather than a directly aggregable number.
SELECT
    "jurisdiction_id",
    "jurisdiction_name",
    "region",
    "indicator",
    "value_text",
    "note",
    "country_url"
FROM "world-prison-brief-current-prison-statistics"
