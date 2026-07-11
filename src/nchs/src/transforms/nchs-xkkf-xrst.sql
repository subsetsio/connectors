-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "week_ending_date",
    "state",
    "observed_number",
    "upper_bound_threshold",
    "exceeds_threshold",
    "average_expected_count",
    "excess_estimate",
    "total_excess_estimate",
    "percent_excess_estimate",
    "year",
    "type",
    "outcome",
    "suppress",
    "note"
FROM "nchs-xkkf-xrst"
