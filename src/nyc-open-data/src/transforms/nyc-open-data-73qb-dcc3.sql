-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_period",
    "first_name",
    "middle_initial",
    "last_name",
    "entity_name",
    "doing_business_start_date",
    "date_removed",
    "db_date_ended"
FROM "nyc-open-data-73qb-dcc3"
