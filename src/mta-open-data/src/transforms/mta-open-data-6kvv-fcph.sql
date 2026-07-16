-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "acep",
    "agency",
    "agency_description",
    "plan_id",
    "category",
    "category_description",
    "element",
    "element_description",
    "needs_code",
    "project",
    "title",
    "description",
    "plan_revision",
    "date",
    "change_nar",
    "year_1_allocation",
    "year_2_allocation",
    "year_3_allocation",
    "year_4_allocation",
    "year_5_allocation",
    "out_years_allocation",
    "total_allocation"
FROM "mta-open-data-6kvv-fcph"
