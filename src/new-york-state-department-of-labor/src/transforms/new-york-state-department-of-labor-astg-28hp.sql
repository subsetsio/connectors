-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Construction fatality records do not expose a stable incident identifier; treat rows as reported events rather than deduplicated persons or employers.
SELECT
    "business_purpose_or_industry",
    "cause_of_death",
    "union_status",
    "city_death_occurred",
    CAST("date_death_occurred" AS TIMESTAMP) AS date_death_occurred,
    "georeference"
FROM "new-york-state-department-of-labor-astg-28hp"
