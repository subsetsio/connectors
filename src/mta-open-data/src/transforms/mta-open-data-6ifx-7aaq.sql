-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "agency_code",
    "category_code",
    "element_code",
    "project_code",
    "acep",
    "agency_name",
    "category_description",
    "element_description",
    "project_title",
    "needs_code",
    "total_budget",
    "parent_acep"
FROM "mta-open-data-6ifx-7aaq"
