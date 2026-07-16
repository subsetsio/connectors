-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "agency",
    "asset",
    "type",
    "total",
    "useful_life",
    "acceptance_date_of_first_cars_accepted",
    "acceptance_date_of_last_cars_accepted"
FROM "mta-open-data-hjck-ty8r"
