-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "agency",
    "asset",
    "total",
    "useful_life",
    "year_built",
    "remaining_useful_life_in_years"
FROM "mta-open-data-vubw-ein5"
