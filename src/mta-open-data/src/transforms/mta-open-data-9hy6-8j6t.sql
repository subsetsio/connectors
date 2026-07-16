-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "project_id",
    "title",
    "stage",
    "phase",
    "agencies",
    "asset_categories",
    "type",
    "description",
    "services",
    "capital_plans",
    "districts",
    "prime_contractor",
    "contract_number",
    "contract_type",
    "initiatives",
    "budget_status",
    "schedule_status",
    "start_date",
    "goal_completion_date",
    "estimated_actual_completion_date",
    "goal_project_cost",
    "estimated_actual_project_cost",
    "search_tags"
FROM "mta-open-data-9hy6-8j6t"
