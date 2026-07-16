-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "indicator_sequence",
    "parent_sequence",
    "agency_name",
    "indicator_name",
    "description",
    "category",
    "frequency",
    "desired_change",
    "indicator_unit",
    "decimal_places",
    "period_year",
    "period_month",
    "ytd_target",
    "ytd_actual",
    "monthly_target",
    "monthly_actual",
    "period"
FROM "mta-open-data-cy9b-i9w9"
