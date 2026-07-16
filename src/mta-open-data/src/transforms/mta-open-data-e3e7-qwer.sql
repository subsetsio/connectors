-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "reference_number",
    "agency",
    "agency_description",
    "type_of_contract",
    "duration_of_contract",
    "contract_description",
    "project_description",
    "solicitation_month",
    "solicitation_year",
    "dollar_range",
    "task_1",
    "task_2",
    "task_3",
    "task_4",
    "task_5",
    "task_6",
    "task_7",
    "task_8",
    "task_9",
    "task_10",
    "task_11",
    "task_12",
    "task_13",
    "task_14"
FROM "mta-open-data-e3e7-qwer"
