-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "project_name",
    "reporting_quarter",
    "entity_name",
    "entity_role",
    "entity_wage_reporting_status",
    "project_wage_reporting_status"
FROM "nyc-open-data-34zf-iv73"
