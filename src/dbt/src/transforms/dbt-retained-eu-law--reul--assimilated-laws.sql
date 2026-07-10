-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable unique row identifier: `reul_name` is nearly unique but the source carries a few duplicate/near-duplicate law records, so no key is declared.
SELECT
    "reul_name",
    "legislation_description",
    "new_lead_dept",
    "type_of_reul",
    "primary_secondary",
    "sector",
    "policy_area",
    "territorial_application_of_reul",
    "international_obligations",
    "reul_status",
    "amendedrepealreplaced",
    "changes_to_reul_details",
    "new_legislation"
FROM "dbt-retained-eu-law--reul--assimilated-laws"
