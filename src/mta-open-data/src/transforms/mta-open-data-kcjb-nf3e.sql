-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "year",
    "name",
    "working_agency",
    "start_date",
    "separation_date",
    "title",
    "department",
    "pay_basis",
    "hourly_rate",
    "regular_pay",
    "overtime_pay",
    "cash_outs",
    "retro_pay",
    "other_pay",
    "total_earnings",
    "updated_at"
FROM "mta-open-data-kcjb-nf3e"
